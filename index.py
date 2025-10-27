from fastapi import FastAPI, Request, HTTPException
import hmac
import hashlib
import json
from datetime import datetime

app = FastAPI()

@app.get("/health")
async def health():
    return {"status": "healthy", "timestamp": datetime.now().isoformat()}

@app.post("/webhook")
async def webhook(request: Request):
    return {"status": "received", "message": "Webhook received successfully"}

@app.get("/")
async def root():
    return {"message": "Smartlead → Notion Webhook Active"}
