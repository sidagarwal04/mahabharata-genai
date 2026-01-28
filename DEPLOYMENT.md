# Deployment Instructions

## Prerequisites
1. GitHub repository pushed with latest changes
2. Render account (render.com)
3. Netlify account (netlify.com)
4. Required API keys and services set up

## Backend Deployment (Render)

### Step 1: Create Render Web Service
1. Go to [render.com](https://render.com) and sign in
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Select your repository: `mahabharata-genai`

### Step 2: Configure Render Service
- **Name**: `mahabharata-backend` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`
- **Root Directory**: `backend`
- **Runtime**: `Python 3.11`
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Set Environment Variables in Render
Go to your service → Environment tab and add these variables (use values from your `backend/example.backend.env` file):

```
NEO4J_URI=your_neo4j_uri_here
NEO4J_USERNAME=your_neo4j_username
NEO4J_PASSWORD=your_neo4j_password_here
NEO4J_DATABASE=neo4j
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
SARVAM_API_KEY=your_sarvam_api_key_here

# Keep-alive configuration (prevents server from sleeping)
RENDER_EXTERNAL_URL=https://your-render-app.onrender.com
```

**Important**: Replace `your-render-app` with your actual Render service name.

### Step 4: Deploy
Click "Create Web Service" - Render will automatically build and deploy your backend.

## Frontend Deployment (Netlify)

### Step 1: Create Netlify Site
1. Go to [netlify.com](https://netlify.com) and sign in
2. Click "Add new site" → "Import an existing project"
3. Choose "Deploy with GitHub"
4. Select your repository: `mahabharata-genai`

### Step 2: Configure Build Settings
- **Base directory**: `frontend`
- **Build command**: `npm run build`
- **Publish directory**: `frontend/dist`

### Step 3: Set Environment Variables in Netlify
Go to Site settings → Environment variables and add:

```
API_BASE_URL=https://your-render-app.onrender.com
```

Replace `your-render-app` with your actual Render service URL.

### Step 4: Deploy
Click "Deploy site" - Netlify will build and deploy your frontend.

## Post-Deployment Steps

1. **Update CORS**: Your backend is already configured to accept requests from any origin (`allow_origins=["*"]`)

2. **Update Frontend API URL**: After your Render backend is deployed, update the `API_BASE_URL` environment variable in Netlify with your Render service URL.

3. **Test the Connection**: Visit your Netlify site and test that it can communicate with your Render backend.

4. **Custom Domains** (Optional):
   - For Render: Add your custom domain in service settings
   - For Netlify: Add your custom domain in site settings

## Monitoring and Logs

- **Render**: View logs in your service dashboard
- **Netlify**: View build logs and function logs in your site dashboard

## Troubleshooting

1. **Build Failures**: Check build logs in respective dashboards
2. **API Connection Issues**: Verify the API_BASE_URL in Netlify environment variables
3. **CORS Issues**: Backend is configured to accept all origins
4. **Environment Variables**: Double-check all required API keys are set correctly

Your app will be available at:
- Backend: `https://your-render-app.onrender.com`
- Frontend: `https://your-netlify-site.netlify.app`