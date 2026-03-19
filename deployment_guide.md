# Deployment Guide for MZCart

This guide explains how to deploy MZCart to **Render**.

## 1. Prerequisites
- A **GitHub** account.
- A **Render** account.
- Your code must be pushed to a GitHub repository.

## 2. Prepare Environment Variables
You will need to set the following variables in the Render Dashboard:

| Variable | Value |
| :--- | :--- |
| `DATABASE_URL` | (Provided by Render PostgreSQL) |
| `SECRET_KEY` | (Your Django secret key) |
| `DEBUG` | `False` |
| `PAYSTACK_PUBLIC_KEY` | (From Paystack Dashboard) |
| `PAYSTACK_SECRET_KEY` | (From Paystack Dashboard) |
| `DJANGO_SETTINGS_MODULE` | `My_Jumia.settings` |

## 3. Step-by-Step Deployment

### Step A: Create a PostgreSQL Database
1. Go to **Render Dashboard** -> **New** -> **PostgreSQL**.
2. Name it `mzcart-db`.
3. Copy the **Internal Database URL** once created.

### Step B: Create a Web Service
1. Go to **Render Dashboard** -> **New** -> **Web Service**.
2. Connect your **MZCart** GitHub repository.
3. Configure settings:
   - **Environment**: `Python`
   - **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
   - **Start Command**: `gunicorn My_Jumia.wsgi:application`
4. Go to **Environment** tab and add the variables from Step 2.
   - Use the `DATABASE_URL` from Step A.

### Step C: Static Files
Render will serve static files via `Whitenoise` (already configured in `settings.py`). The build command handles `collectstatic`.

## 4. Finalizing
Once the deployment is green:
1. Create a superuser to access the admin and vendor verification:
   - Go to **Render Dashboard** -> **Web Service** -> **Shell**.
   - Run: `python manage.py createsuperuser`.
2. Access your site at `https://your-app-name.onrender.com`.

---
*Senior Dev Tip: Always monitor your logs in the Render Dashboard for any startup errors.*
