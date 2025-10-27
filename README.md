# Smartlead → Notion Webhook Integration

Automatic webhook integration to sync Smartlead campaign events to Notion.

## Configuration

**Notion Database ID:** 29968cdd-cdbd-813d-8fc9-ecd2a3dab083

## Environment Variables

Set these in Vercel Settings → Environment Variables:

- `NOTION_DATABASE_ID` = 29968cdd-cdbd-813d-8fc9-ecd2a3dab083
- `NOTION_API_KEY` = Your Notion integration token
- `SMARTLEAD_WEBHOOK_SECRET` = Your Smartlead webhook secret
- `COMPOSIO_API_KEY` = Your Composio API key

## Local Testing

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
uvicorn api.webhook:app --reload

# Test health check
curl http://localhost:8000/health
```

## Deployment

Deployed to Vercel - automatic deployments on git push.

## Webhook URL

After deployment:
```
https://[your-vercel-project].vercel.app/api/webhook
```

## Features

- ✅ Automatic event capture from Smartlead
- ✅ Real-time sync to Notion (< 1 second)
- ✅ HMAC-SHA256 signature verification
- ✅ Automatic retries with exponential backoff
- ✅ 14 fields automatically populated
- ✅ Production-ready error handling

## Support

See DEPLOYMENT_INSTRUCTIONS.md for detailed setup instructions.
