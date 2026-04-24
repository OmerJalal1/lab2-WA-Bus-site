# Bus Network - Deployment Guide to Render

## Prerequisites
- GitHub account with your code pushed
- Render account (render.com)
- Your project must have the following files:
  - `requirements.txt` - Python dependencies
  - `runtime.txt` - Python version
  - `Procfile` - How to run the app
  - `.env.example` - Environment variables template

## Step 1: Prepare Your Repository

1. Make sure all your code is committed and pushed to GitHub:
```bash
git add .
git commit -m "Ready for Render deployment"
git push origin main
```

2. Create a `.env` file with your secret key (DO NOT push this to GitHub):
```bash
# Generate a new SECRET_KEY
python manage.py shell
>>> from django.core.management.utils import get_random_secret_key
>>> print(get_random_secret_key())
```

3. Update `.gitignore` to exclude `.env` and other sensitive files (already done).

## Step 2: Create a PostgreSQL Database on Render

1. Go to [render.com](https://render.com) and log in
2. Click "New +" → "PostgreSQL"
3. Fill in the details:
   - **Name**: `buses-db` (or your preference)
   - **Database**: `buses_db`
   - **User**: `postgres` (default)
   - **Region**: Select your closest region
   - **PostgreSQL Version**: 15
4. Click "Create Database"
5. Copy the internal database URL (you'll need this later)

## Step 3: Deploy Your Django App

1. From Render dashboard, click "New +" → "Web Service"
2. Select "Deploy from a Git repository"
3. Connect your GitHub account and select your repository
4. Fill in the deployment settings:
   - **Name**: `buses-network` (or your preference)
   - **Environment**: `Python 3.11`
   - **Region**: Same as database region (important for performance)
   - **Build Command**: `pip install -r requirements.txt && python manage.py migrate && python manage.py collectstatic --noinput`
   - **Start Command**: `gunicorn buses_project.wsgi:application`

5. Click "Advanced" and add these Environment Variables:
   - `SECRET_KEY`: Your generated secret key
   - `DEBUG`: `False`
   - `DATABASE_URL`: Paste the internal database URL from PostgreSQL
   - `RENDER`: `True`

6. Click "Create Web Service"
7. Render will automatically build and deploy your app. Wait for it to complete.

## Step 4: Create a Superuser on Render

After deployment completes:

1. Go to your Web Service on Render
2. Click "Shell" tab
3. Run these commands:
```bash
python manage.py createsuperuser
```

4. Follow the prompts to create an admin user

## Step 5: Access Your App

Your app is now live! 
- **Main app**: `https://your-app-name.onrender.com`
- **Admin panel**: `https://your-app-name.onrender.com/admin`

## Step 6: Add Routes

1. Visit the admin panel at `/admin`
2. Login with your superuser credentials
3. Click "Stations" and add your stations:
   - Central (Ramadi)
   - University (Ramadi)
   - Downtown (Baghdad)
   - Airport (Baghdad)

4. Click "Routes" and add routes connecting stations (choose duration in minutes)

## Features Available

✅ **User Authentication**
- Register new account
- Login/Logout
- Password confirmation on registration

✅ **Browsing Routes**
- View all routes with origin, destination, duration
- See number of passengers booked
- Search/filter routes by origin or destination
- Click station names to see all routes to/from that station

✅ **Booking**
- Only logged-in users can book
- View your booked routes on "My Routes" page
- Cancel bookings with one click
- See all passengers on each route

✅ **Station Details**
- View all routes departing from a station
- View all routes arriving at a station
- Click to book any route directly from station page

✅ **Responsive Design**
- Works on desktop, tablet, and mobile
- Beautiful gradient UI with smooth animations
- Professional styling with Bootstrap 5

## Troubleshooting

### Database Connection Issues
- Check that DATABASE_URL is correctly set in Environment Variables
- Make sure your PostgreSQL database is in the same region as your web service
- Try redeploying: Settings → Redeploy Latest Commit

### Static Files Not Loading
- Run: `python manage.py collectstatic --noinput` locally
- Verify whitenoise is in requirements.txt
- Check that STATIC_ROOT and STATICFILES_STORAGE are set in settings.py

### 500 Server Errors
1. Check logs: Go to Web Service → Logs
2. Common causes:
   - Missing SECRET_KEY in Environment Variables
   - DEBUG=True in production (should be False)
   - Database not migrated
   - Missing environment variables

### App Too Slow
- Render free tier has limited resources
- Consider upgrading to a paid plan
- Optimize database queries
- Ensure PostgreSQL is in same region

## Security Notes

⚠️ **Important for Production:**
- Never commit `.env` file
- Always use `DEBUG=False` on Render
- Use strong SECRET_KEY (generate with Django)
- Enable HTTPS (automatic on Render)
- Regularly update dependencies: `pip list --outdated`

## Monitoring

Monitor your app on Render:
- **Logs**: Real-time application logs
- **Metrics**: CPU, Memory, Bandwidth usage
- **Notifications**: Email alerts for errors

## Additional Resources

- [Render Django Deployment Guide](https://render.com/docs/deploy-django)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/6.0/deployment/checklist/)
- [WhiteNoise Static Files](http://whitenoise.evans.io/)

---

Happy deploying! 🚀
