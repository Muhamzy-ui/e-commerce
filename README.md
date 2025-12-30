# MZ Cart

**Author:** Mahmud Bashir Olasunkanmi  
**Project:** E-commerce Web Application  

MZ Cart is a full-featured e-commerce web application built with **Django** and **PostgreSQL**. It allows users to browse products, add items to a cart, and make payments. The project also includes an admin panel for managing products, orders, and users.

---

This README includes:  
- Project overview and features  
- Installation and setup instructions  
- Environment variables  
- Deployment notes  
- Contribution and license info  


## Features

- User registration and authentication
- Product catalog with categories
- Shopping cart functionality
- Order management
- Payment integration (Paystack)
- Admin dashboard for managing products and orders
- Email notifications
- Responsive design for mobile and desktop

---

## Technologies Used

- Python 3.x
- Django
- PostgreSQL
- HTML, CSS, JavaScript
- Bootstrap (for styling)
- Paystack API for payments

---

## Installation

1. **Clone the repository:**
```bash
git clone https://github.com/Muhamzy-ui/e-commerce.git
cd e-commerce

Create a virtual environment:
python -m venv .venv
.venv\Scripts\activate       # Windows

Install dependencies:
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory with the following:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
PAYSTACK_PUBLIC_KEY=your_paystack_public_key
PAYSTACK_SECRET_KEY=your_paystack_secret_key
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

Run migrations:
python manage.py migrate

Collect static files (for production):
python manage.py collectstatic

Run the development server:
python manage.py runserver

Deployment:

This project can be deployed on Render, Heroku, or any platform that supports Django. Make sure to:

Set all required environment variables

Use PostgreSQL for production

Run collectstatic before deploying

Contributing:

If you want to contribute:

Fork the repository

Create a new branch

Make your changes

Submit a pull request

License:

This project is licensed under the MIT License.

Author

Mahmud Bashir Olasunkanmi
GitHub: https://github.com/Muhamzy-ui

Create a virtual environment:
python -m venv .venv
source .venv/bin/activate    # Linux/Mac
.venv\Scripts\activate       # Windows

Install dependencies:
pip install -r requirements.txt
Set up environment variables:
Create a .env file in the root directory with the following:
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=your_database_url
PAYSTACK_PUBLIC_KEY=your_paystack_public_key
PAYSTACK_SECRET_KEY=your_paystack_secret_key
EMAIL_HOST_USER=your_email@example.com
EMAIL_HOST_PASSWORD=your_email_password

Run migrations:
python manage.py migrate

Collect static files (for production):
python manage.py collectstatic

Run the development server:
python manage.py runserver

Deployment:

This project can be deployed on Render, Heroku, or any platform that supports Django. Make sure to:

Set all required environment variables

Use PostgreSQL for production

Run collectstatic before deploying

Contributing:

If you want to contribute:

Fork the repository

Create a new branch

Make your changes

Submit a pull request

License:

This project is licensed under the MIT License.

Author

Mahmud Bashir Olasunkanmi
GitHub: https://github.com/Muhamzy-ui
