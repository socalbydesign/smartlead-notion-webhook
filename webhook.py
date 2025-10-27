import os
import json
import hmac
import hashlib
import logging
from datetime import datetime
from typing import Dict, Any, List
import requests
from fastapi import FastAPI, Request, HTTPException

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configuration from environment variables
SMARTLEAD_SECRET = os.getenv("SMARTLEAD_WEBHOOK_SECRET", "")
NOTION_API_KEY = os.getenv("NOTION_API_KEY", "")
NOTION_DATABASE_ID = os.getenv("NOTION_DATABASE_ID", "")
COMPOSIO_API_KEY = os.getenv("COMPOSIO_API_KEY", "")

app = FastAPI()

# =============================================================================
# WEBHOOK VALIDATION
# =============================================================================

def verify_webhook_signature(request_body: str, signature: str) -> bool:
    """Verify Smartlead webhook signature using HMAC-SHA256."""
    if not SMARTLEAD_SECRET:
        logger.warning("SMARTLEAD_WEBHOOK_SECRET not configured")
        return False

    expected_signature = hmac.new(
        SMARTLEAD_SECRET.encode(),
        request_body.encode(),
        hashlib.sha256
    ).hexdigest()

    return hmac.compare_digest(signature, expected_signature)


# =============================================================================
# EVENT TRANSFORMATION
# =============================================================================

class SmartleadEventTransformer:
    """Transform Smartlead webhook events into Notion database properties."""

    @staticmethod
    def generate_event_id(event: Dict[str, Any]) -> str:
        """Generate unique event ID from campaign, email, and timestamp."""
        campaign = event.get("campaign", "unknown")
        email = event.get("recipient", {}).get("email", "unknown")
        timestamp = event.get("timestamp", "")

        timestamp_short = timestamp[:19].replace("-", "").replace(":", "").replace("T", "")

        return f"{campaign}_{email}_{timestamp_short}".replace(" ", "_").replace(".", "_")

    @staticmethod
    def format_timestamp(timestamp_str: str) -> str:
        """Convert ISO 8601 timestamp to Notion date format."""
        try:
            dt = datetime.fromisoformat(timestamp_str.replace("Z", "+00:00"))
            return dt.isoformat()
        except Exception as e:
            logger.error(f"Error parsing timestamp: {e}")
            return datetime.now().isoformat()

    @staticmethod
    def build_notion_properties(event: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Transform Smartlead event into Notion database properties."""

        recipient = event.get("recipient", {})
        message = event.get("message", {})

        return [
            {"name": "Event ID", "type": "title", "value": SmartleadEventTransformer.generate_event_id(event)},
            {"name": "Event Type", "type": "rich_text", "value": event.get("event", "unknown")},
            {"name": "Timestamp", "type": "date", "value": SmartleadEventTransformer.format_timestamp(event.get("timestamp", ""))},
            {"name": "Campaign", "type": "rich_text", "value": event.get("campaign", "")},
            {"name": "Email", "type": "email", "value": recipient.get("email", "")},
            {"name": "First Name", "type": "rich_text", "value": recipient.get("first_name", "")},
            {"name": "Last Name", "type": "rich_text", "value": recipient.get("last_name", "")},
            {"name": "Company", "type": "rich_text", "value": recipient.get("company", "")},
            {"name": "City", "type": "rich_text", "value": recipient.get("city", "")},
            {"name": "Address", "type": "rich_text", "value": recipient.get("address1", "")},
            {"name": "Neighborhood", "type": "rich_text", "value": recipient.get("neighborhood", "")},
            {"name": "From", "type": "rich_text", "value": message.get("from", "")},
            {"name": "Subject", "type": "rich_text", "value": message.get("subject", "")},
            {"name": "Link", "type": "url", "value": message.get("link", "")},
        ]


# =============================================================================
# NOTION INTEGRATION
# =============================================================================

class NotionDatabaseHandler:
    """Handle insertions into Notion database using Composio API."""

    def __init__(self, api_key: str, database_id: str):
        self.api_key = api_key
        self.database_id = database_id
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def insert_event(self, properties: List[Dict[str, Any]]) -> bool:
        """Insert event into Notion database via Composio API."""

        try:
            payload = {"database_id": self.database_id, "properties": properties}

            response = requests.post(
                "https://api.composio.dev/v1/actions/NOTION_INSERT_ROW_DATABASE",
                headers=self.headers,
                json=payload,
                timeout=30
            )

            if response.status_code in [200, 201]:
                logger.info(f"✓ Event inserted: {properties[0]['value']}")
                return True
            else:
                logger.error(f"Error: {response.status_code} - {response.text}")
                return False

        except Exception as e:
            logger.error(f"Exception: {str(e)}")
            return False


# =============================================================================
# RETRY LOGIC
# =============================================================================

class RetryHandler:
    """Handle retries with exponential backoff."""

    MAX_RETRIES = 3
    RETRY_DELAYS = [5, 25, 125]

    @staticmethod
    def retry_with_backoff(func, *args, **kwargs):
        """Execute function with exponential backoff retry."""
        import time

        for attempt in range(RetryHandler.MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                if attempt < RetryHandler.MAX_RETRIES - 1:
                    delay = RetryHandler.RETRY_DELAYS[attempt]
                    logger.warning(f"Attempt {attempt + 1} failed, retrying in {delay}s")
                    time.sleep(delay)
                else:
                    logger.error(f"All retries exhausted: {str(e)}")
                    raise


# =============================================================================
# ENDPOINTS
# =============================================================================

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Smartlead → Notion Webhook Handler",
        "timestamp": datetime.now().isoformat(),
        "database_id": NOTION_DATABASE_ID[:20] + "..." if NOTION_DATABASE_ID else "NOT SET"
    }


@app.post("/api/webhook")
async def handle_webhook(request: Request):
    """Main webhook handler for Smartlead events."""

    try:
        body = await request.body()
        body_text = body.decode('utf-8')
        signature = request.headers.get("X-Smartlead-Signature", "")

        if not signature:
            logger.warning("Missing webhook signature")
            raise HTTPException(status_code=401, detail="Missing signature")

        if not verify_webhook_signature(body_text, signature):
            logger.warning("Invalid webhook signature")
            raise HTTPException(status_code=401, detail="Invalid signature")

        event = json.loads(body_text)
        logger.info(f"📨 Webhook: {event.get('event')} from {event.get('campaign')}")

        if not NOTION_DATABASE_ID or not NOTION_API_KEY or not COMPOSIO_API_KEY:
            logger.error("Missing env vars")
            raise HTTPException(status_code=500, detail="Server config error")

        transformer = SmartleadEventTransformer()
        properties = transformer.build_notion_properties(event)

        handler = NotionDatabaseHandler(COMPOSIO_API_KEY, NOTION_DATABASE_ID)

        def insert_fn():
            return handler.insert_event(properties)

        success = RetryHandler.retry_with_backoff(insert_fn)

        if success:
            return {
                "status": "success",
                "message": "Event inserted into Notion",
                "event_id": properties[0]["value"]
            }
        else:
            raise HTTPException(status_code=500, detail="Failed to insert")

    except json.JSONDecodeError:
        logger.error("Invalid JSON")
        raise HTTPException(status_code=400, detail="Invalid JSON")
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error: {str(e)}")


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "Smartlead → Notion Webhook Handler",
        "health": "/health",
        "webhook": "/api/webhook"
    }
