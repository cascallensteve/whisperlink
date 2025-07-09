# Vercel Deployment Guide for WhisperLink

This guide explains how to deploy your WhisperLink Django application to Vercel.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com)
2. **GitHub Repository**: Push your code to GitHub
3. **Supabase Database**: Your PostgreSQL database should be accessible from Vercel

## Files Added for Vercel Deployment

### 1. `vercel.json` - Vercel Configuration
```json
{
  "version": 2,
  "builds": [
    {
      "src": "whisperlink_backend/wsgi.py",
      "use": "@vercel/python",
      "config": { "maxLambdaSize": "15mb", "runtime": "python3.9" }
    }
  ],
  "routes": [
    {
      "src": "/static/(.*)",
      "dest": "/feedback/static/$1"
    },
    {
      "src": "/(.*)",
      "dest": "whisperlink_backend/wsgi.py"
    }
  ]
}
```

### 2. `requirements.txt` - Python Dependencies
```
Django==4.2.7
psycopg2-binary==2.9.9
requests==2.31.0
python-dotenv==1.0.0
whitenoise==6.6.0
gunicorn==21.2.0
```

### 3. `build_files.sh` - Build Script
```bash
#!/bin/bash
pip install -r requirements.txt
python manage.py collectstatic --noinput
python manage.py migrate --noinput
```

## Environment Variables Setup

### Required Environment Variables in Vercel

1. **Django Configuration**
   - `SECRET_KEY`: Django secret key (generate a new one for production)
   - `DEBUG`: Set to `False` for production
   - `ALLOWED_HOST`: Your Vercel domain (e.g., `myapp.vercel.app`)

2. **Database Configuration**
   - `DB_NAME`: postgres
   - `DB_USER`: postgres.rpptvbcjrytijmfqvndj
   - `DB_PASSWORD`: Stevoh@Stevoh2020.
   - `DB_HOST`: aws-0-eu-north-1.pooler.supabase.com
   - `DB_PORT`: 6543

3. **Email Configuration**
   - `EMAIL_HOST_USER`: Your Gmail address
   - `EMAIL_HOST_PASSWORD`: Your Gmail app password

4. **AI Configuration**
   - `TOGETHER_API_KEY`: Your Together AI API key

## Deployment Steps

### Step 1: Prepare Your Repository
1. Push all files to your GitHub repository
2. Make sure `vercel.json` is in the root of your project
3. Ensure all required files are committed

### Step 2: Connect to Vercel
1. Go to [vercel.com](https://vercel.com)
2. Sign in with your GitHub account
3. Click "New Project"
4. Select your WhisperLink repository
5. Set the root directory to `whisperlink/backend`

### Step 3: Configure Environment Variables
1. In Vercel dashboard, go to your project settings
2. Click "Environment Variables"
3. Add all the required variables listed above
4. Make sure to set `DEBUG=False` for production

### Step 4: Deploy
1. Click "Deploy" in Vercel
2. Wait for the build to complete
3. Test your deployed application

## Important Configuration Changes Made

### 1. Static Files Handling
- Added WhiteNoise middleware for static file serving
- Configured `STATIC_ROOT` for collected static files
- Updated `STATICFILES_STORAGE` for compression

### 2. Database Configuration
- Made database settings configurable via environment variables
- Added connection timeout for better reliability
- Maintained SSL requirement for Supabase

### 3. Security Settings
- Made `SECRET_KEY` configurable via environment variable
- Set `DEBUG=False` for production
- Configured `ALLOWED_HOSTS` for Vercel domains

### 4. Error Handling
- Custom error handling system works with Vercel
- Database connection errors are handled gracefully
- Health check endpoint available at `/health/`

## Testing Your Deployment

### 1. Basic Functionality
- Visit your Vercel URL
- Test user registration and login
- Try the password reset functionality
- Submit feedback through the forms

### 2. Health Check
- Visit `/health/` to check database connectivity
- Should return JSON with database status

### 3. Static Files
- Verify CSS and JavaScript are loading correctly
- Check that icons and images display properly

## Troubleshooting

### Common Issues

1. **Build Failures**
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version compatibility
   - Check build logs in Vercel dashboard

2. **Database Connection Issues**
   - Verify all database environment variables are set correctly
   - Check that your Supabase database allows connections from Vercel
   - Test connection using the health check endpoint

3. **Static Files Not Loading**
   - Ensure WhiteNoise is properly configured
   - Check that `STATIC_ROOT` is set correctly
   - Verify static files are being collected during build

4. **Environment Variables**
   - Make sure all required variables are set in Vercel
   - Check for typos in variable names
   - Verify that sensitive data is not hardcoded

### Debugging Steps

1. **Check Vercel Build Logs**
   - Look for errors during the build process
   - Check if migrations ran successfully
   - Verify static files were collected

2. **Test Database Connection**
   - Use the `/health/` endpoint to verify database connectivity
   - Check Supabase logs for connection attempts
   - Verify database credentials in environment variables

3. **Check Application Logs**
   - Monitor Vercel function logs for runtime errors
   - Look for database timeout errors
   - Check for missing environment variables

## Post-Deployment Checklist

- [ ] All environment variables are set
- [ ] Database connection is working
- [ ] Static files are loading correctly
- [ ] User registration and login work
- [ ] Password reset emails are being sent
- [ ] AI feedback generation is working
- [ ] Error pages display correctly
- [ ] Health check endpoint responds correctly

## Maintenance

### Regular Tasks
1. **Monitor Performance**: Check Vercel analytics for performance metrics
2. **Update Dependencies**: Keep Python packages updated
3. **Database Monitoring**: Monitor Supabase for connection issues
4. **Security Updates**: Keep Django and dependencies updated

### Scaling Considerations
- Vercel automatically scales serverless functions
- Monitor database connection limits in Supabase
- Consider upgrading Supabase plan if needed
- Implement caching for better performance

## Support

If you encounter issues:
1. Check Vercel documentation for Django deployments
2. Review Supabase connection settings
3. Monitor application logs for specific errors
4. Test locally with production settings first

Your WhisperLink application is now ready for production deployment on Vercel!
