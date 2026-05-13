# 🛒 StyleHub — Production-Ready Django Shopping Website

A fully production-ready eCommerce website built with **Django**, featuring real cart logic, a complete backend, a rich database model, and real content throughout.

---

## ✨ Features

| Feature | Details |
|---|---|
| **Real Cart** | Session-based cart with AJAX add / update / remove — no page reloads |
| **Django Backend** | Models, views, URL routing, admin panel, context processors |
| **Real Products** | 16 seeded products with real photos, descriptions, prices, stock tracking |
| **Real Blog** | 5 full articles with real fashion content |
| **Real About/Contact** | No lorem ipsum — all genuine copy |
| **Checkout + Orders** | Full checkout form, order creation, stock deduction, success page |
| **Newsletter** | Email subscribe API with DB persistence |
| **Contact Form** | Messages saved to DB, readable in admin |
| **Django Admin** | Full admin panel for all models |
| **Responsive** | Mobile-first, works on all screen sizes |
| **Toast Notifications** | Animated feedback for all cart/form actions |
| **Filter & Search** | Filter by category, gender, price; sort by newest/price/rating |

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- pip

### 2. Set up virtual environment
```bash
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install django

```

### 3. Install dependencies
```bash
pip install -r requirements.txt
pip install pillow
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Seed the database (products + blog posts)
```bash
python manage.py seed_data
```

### 6. Create an admin user
```bash
python manage.py createsuperuser
```

### 7. Start the server
```bash
python manage.py runserver
```

### 8. Open in browser
- **Website:** http://127.0.0.1:8000/
- **Admin panel:** http://127.0.0.1:8000/admin/

---

## 📁 Project Structure

```
shop/
├── manage.py
├── requirements.txt
├── shopproject/              # Django project config
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── store/                    # Main app
│   ├── models.py             # All DB models
│   ├── views.py              # All page + API views
│   ├── urls.py               # URL patterns
│   ├── admin.py              # Admin registrations
│   ├── context_processors.py # Cart count everywhere
│   ├── management/
│   │   └── commands/
│   │       └── seed_data.py  # Data seeder
│   ├── templates/store/      # All HTML templates
│   │   ├── base.html
│   │   ├── index.html        # Home
│   │   ├── shop.html         # Product listing + filters
│   │   ├── product.html      # Product detail
│   │   ├── cart.html         # Cart (AJAX)
│   │   ├── checkout.html     # Checkout form
│   │   ├── order_success.html
│   │   ├── about.html
│   │   ├── contact.html
│   │   ├── blog.html
│   │   ├── blog_detail.html
│   │   └── partials/
│   │       └── product_card.html
│   └── static/store/
│       ├── css/main.css      # Full production CSS
│       └── js/main.js        # Cart JS + toast + mobile nav
├── media/                    # Uploaded product images
└── db.sqlite3                # Auto-created SQLite database
```

---

## 🔌 API Endpoints

| Method | URL | Description |
|---|---|---|
| `POST` | `/api/cart/add/` | Add item to cart |
| `POST` | `/api/cart/update/` | Update item quantity |
| `POST` | `/api/cart/remove/` | Remove item from cart |
| `POST` | `/api/newsletter/` | Subscribe to newsletter |

All cart APIs use session-based carts (no login required).

---

## ⚙️ Django Admin

Login at `/admin/` to manage:
- **Products** — add, edit, set featured/new arrival, manage stock
- **Orders** — view all orders, update status
- **Blog Posts** — publish/unpublish articles
- **Newsletter Subscribers** — view email list
- **Contact Messages** — mark as read/unread
- **Categories** — manage product categories

---

## 🚢 Production Deployment Checklist

1. Set `DEBUG = False` in `settings.py`
2. Set a strong `SECRET_KEY` (use environment variable)
3. Configure `ALLOWED_HOSTS` with your domain
4. Set up PostgreSQL instead of SQLite
5. Configure email backend (e.g. SendGrid, Mailgun)
6. Run `python manage.py collectstatic`
7. Use Gunicorn + Nginx in production
8. Enable HTTPS with Let's Encrypt

---

## 📦 Models

- **Category** — Product categories with slugs
- **Product** — Full product with price, stock, images, sizes, ratings
- **ProductImage** — Multiple images per product
- **Cart** — Session-linked cart
- **CartItem** — Items in cart with quantity and size
- **Order** — Full order with shipping details and status
- **OrderItem** — Snapshot of product at time of purchase
- **BlogPost** — Full blog articles
- **ContactMessage** — Contact form submissions
- **NewsletterSubscriber** — Email subscribers
