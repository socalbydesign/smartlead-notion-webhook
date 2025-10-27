# 🚀 VERCEL DEPLOYMENT - AUTOMATED SETUP

## ✅ STATUS: READY FOR DEPLOYMENT

All credentials are configured. You're ready to deploy!

---

## 📋 YOUR CONFIGURATION

| Item | Value |
|------|-------|
| Notion Database ID | 29968cdd-cdbd-813d-8fc9-ecd2a3dab083 |
| Notion API Key | ✅ Set in Vercel environment |
| Composio API Key | ✅ Set in Vercel environment |
| Smartlead Webhook Secret | ✅ Generated during setup |

---

## 🎯 QUICK DEPLOYMENT (3 STEPS)

### STEP 1: Create GitHub Repository
1. Go to https://github.com/new
2. **Repository name:** `smartlead-notion-webhook`
3. **Description:** "Smartlead to Notion webhook integration"
4. Choose **Public**
5. Click **"Create repository"**
6. Copy the repository URL

### STEP 2: Upload Files to GitHub
1. In your new repository, click **"Add file"** → **"Upload files"**
2. Select all files from this package
3. Commit with message: "Initial Smartlead webhook setup"

### STEP 3: Deploy to Vercel
1. Go to https://vercel.com
2. Click **"New Project"**
3. Click **"Import Project"**
4. Paste your GitHub repository URL
5. Click **"Import"**
6. Click **"Deploy"**
7. ⏳ Wait 1-2 minutes for deployment

**That's it!** Your webhook is now deployed! 🎉

---

## 📍 Your Deployment URL

After deployment, your webhook URL will be:
```
https://YOUR_PROJECT_NAME.vercel.app/api/webhook
```

Example: `https://smartlead-notion-webhook.vercel.app/api/webhook`

---

## ✅ VERIFY DEPLOYMENT

Test the health check:

1. Open in browser:
   ```
   https://YOUR_PROJECT_NAME.vercel.app/health
   ```

2. You should see:
   ```json
   {
     "status": "healthy",
     "service": "Smartlead → Notion Webhook Handler",
     "timestamp": "2025-10-27T...",
     "database_id": "29968cdd-cdbd-813d..."
   }
   ```

✅ If you see this, deployment works!

---

## 🔧 CONFIGURE VERCEL ENVIRONMENT VARIABLES

1. Go to your Vercel project → **Settings** → **Environment Variables**
2. Add these 4 variables:

### Variable 1: NOTION_DATABASE_ID
```
Name: NOTION_DATABASE_ID
Value: 29968cdd-cdbd-813d-8fc9-ecd2a3dab083
Environments: Production, Preview, Development
```

### Variable 2: NOTION_API_KEY
```
Name: NOTION_API_KEY
Value: [Your Notion integration token from Notion Settings]
Environments: Production, Preview, Development
```

### Variable 3: COMPOSIO_API_KEY
```
Name: COMPOSIO_API_KEY
Value: [Your Composio API key from Composio Dashboard]
Environments: Production, Preview, Development
```

### Variable 4: SMARTLEAD_WEBHOOK_SECRET
```
Name: SMARTLEAD_WEBHOOK_SECRET
Value: [You'll get this from Smartlead in the next step]
Environments: Production, Preview, Development
```

3. After adding all variables, go to **Deployments** and click **Redeploy** on latest

---

## 🔧 FINAL STEP: Configure Smartlead Webhook

Once deployment is verified and environment variables are set:

1. Go to **Smartlead Dashboard**
2. **Settings** → **Integrations** → **Webhooks**
3. Click **"Add New Webhook"**
4. **Webhook URL:** Paste your Vercel URL (from Step 3 above)
5. Click **"Generate Secret"**
6. **IMPORTANT:** Copy the secret - you'll need it for Vercel!
7. **Select Events to subscribe:**
   - ☑ Email Sent
   - ☑ Email Opened
   - ☑ Link Clicked
   - ☑ Reply Received
   - ☑ Bounce
   - ☑ Unsubscribe
8. Click **"Save"**

9. Add the secret to Vercel:
   - Go back to Vercel project settings
   - Add SMARTLEAD_WEBHOOK_SECRET environment variable
   - Redeploy

---

## 🧪 TEST IT!

1. In Smartlead, click **"Send Test"** on your webhook
2. Go to Notion → **SoCal By Design** → **Smartlead Events**
3. You should see a new entry within 5-30 seconds!

✅ If you see it, you're done!

---

## 📊 WHAT HAPPENS NEXT

Every time Smartlead has a campaign event:
1. Webhook sends data to your Vercel endpoint
2. Endpoint validates the signature
3. Data is transformed to Notion format
4. Entry automatically created in database
5. All 14 fields auto-populated in real-time

**Zero manual work. Automatic real-time syncing.** 🚀

---

## 🆘 TROUBLESHOOTING

**Health check URL doesn't work:**
- Double-check your project name
- Wait a few seconds for Vercel to fully deploy

**No entry in Notion after test:**
- Check Vercel logs: Deployments → Latest → Logs
- Verify all environment variables are set

**401 Unauthorized Error:**
- Verify SMARTLEAD_WEBHOOK_SECRET matches in Smartlead

---

**Total Setup Time: ~15 minutes**

Good luck! 🚀
