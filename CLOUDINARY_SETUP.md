# Cloudinary Setup Guide

## 1. Create a Free Cloudinary Account

1. Go to [https://cloudinary.com](https://cloudinary.com)
2. Click **"Sign Up Free"**
3. Sign up with GitHub, Google, or email
4. Verify your email

## 2. Get Your Credentials

After signing in:

1. Go to **Dashboard** (top menu)
2. Copy these three values:
   - **Cloud Name** (e.g., `dxxxxx`)
   - **API Key** (e.g., `123456789012345`)
   - **API Secret** (e.g., `abc123def456...`) - click "Reveal" to see it

## 3. Add Credentials to Render

1. Go to your Render dashboard
2. Click on your service → **Environment**
3. Add these three variables:

| Key | Value |
|-----|-------|
| `CLOUDINARY_CLOUD_NAME` | Your cloud name from dashboard |
| `CLOUDINARY_API_KEY` | Your API key |
| `CLOUDINARY_API_SECRET` | Your API secret |

## 4. Migrate Existing Media Files (Optional)

If you already have images in your local `media/` folder, upload them manually:

1. In Cloudinary Dashboard, go to **Media Library**
2. Click **Upload** → **Upload files**
3. Upload your images to the appropriate folders:
   - `notes/subjects/`
   - `notes/chapters/`
   - `notes/topics/`
   - `notes/uploads/`

Or use the upload API for bulk uploads.

## 5. Redeploy

After adding the environment variables:

1. Go to Render dashboard
2. Click **Manual Deploy** → **Deploy latest commit**
3. Wait for deployment to complete

## Free Tier Limits

| Feature | Limit |
|---------|-------|
| Storage | 25 GB |
| Bandwidth | 25 GB/month |
| Transformations | 25,000/month |
| Uploads | Unlimited |

This is enough for thousands of note images!
