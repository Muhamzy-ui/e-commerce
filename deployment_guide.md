# 🚀 MZCart: The Ultimate Deployment Guide

Follow these steps exactly to move your project from your computer to the web using **Render** (Hosting) and **Supabase** (Database).

---

## 💎 Step 1: Create Your Database (Supabase)
Since Render's free tier only allows one database, we use **Supabase** to get a dedicated, powerful PostgreSQL database for free.

1.  Go to [Supabase.com](https://supabase.com/) and sign in with GitHub.
2.  Click **"New Project"**.
3.  **Name**: `MZCart-DB`
4.  **Database Password**: Create a strong password and **COPY IT**.
5.  **Region**: Select the region closest to you (e.g., `London` or `East US`).
6.  Wait 2 minutes for the database to start.
7.  Go to **Project Settings** (Gear icon ⚙️) -> **Database**.
8.  Find the **Connection string** section. 
9.  Click the **URI** tab. It looks like this: `postgresql://postgres:[YOUR-PASSWORD]@db.xxxx.supabase.co:5432/postgres`
10. **REPLACE** `[YOUR-PASSWORD]` with the password you created in step 4.
11. **KEEP THIS URI READY.** This is your `DATABASE_URL`.

---

## 🛠️ Step 2: Prepare Your Code
I have already updated your `requirements.txt`, `settings.py`, and created a `Procfile`.

1.  Open your terminal in VS Code.
2.  Run these commands to make sure everything is saved:
    ```bash
    git add .
    git commit -m "Final production preparation"
    git push
    ```

---

## 🌍 Step 3: Deploy to Render
1.  Go to [Render.com](https://render.com/) and sign in.
2.  Click **"New +"** -> **Web Service**.
3.  Connect your GitHub repository: `Muhamzy-ui/e-commerce`.
4.  **Name**: `mzcart-elite` (or anything you like).
5.  **Environment**: `Python 3`
6.  **Build Command**: `pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate`
7.  **Start Command**: `gunicorn My_Jumia.wsgi:application`

---

## 🔑 Step 4: Add Environment Variables
This is the most critical part. In Render, click the **Environment** tab and add these:

| Key | Value |
| :--- | :--- |
| `DATABASE_URL` | *Paste your Supabase URI from Step 1* (URI tab) |
| `SECRET_KEY` | *Generate a random long string* |
| `DEBUG` | `False` |
| `PYTHON_VERSION` | `3.13.7` |

---

## ✅ Step 5: Final Check
1.  Click **"Deploy Web Service"**.
2.  Watch the logs. Once it says **"Live"**, click the URL at the top left (it looks like `mzcart-elite.onrender.com`).

### 🥇 Troubleshooting
- If the CSS looks broken: Make sure `WHITENOISE` is in `MIDDLEWARE` in `settings.py`. (I have already done this for you!)
- If you get a "Database Connection" error: Double-check your `DATABASE_URL` password.

**Welcome to the web, MZCart!** 🏆
