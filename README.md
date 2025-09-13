# 🛒 Ecom Backend

A **Django + Django REST Framework (DRF)** backend for an e-commerce application.  
It provides APIs for **users, products, categories, cart, orders, and Razorpay payment integration**.

---

## 🚀 Features

- User authentication (JWT/DRF token-based)  
- Product & product variant management  
- Cart (add, update, delete items)  
- Order creation with Razorpay integration  
- Payment verification  
- API-first design (fully testable with Postman collection included)  

---

## 📂 Project Structure

```
Ecom/
│── Buying/         # Cart & Order logic
│── categories/     # Categories app
│── mainfold/       # Project settings and root urls
│── products/       # Products and variants
│── users/          # Custom user app
│── venv/           # Virtual environment (ignored in git)
│── db.sqlite3      # Local SQLite database
│── manage.py
│── requirements.txt
```

---

## 🛠 Installation

### 1. Clone the repository
```bash
git clone https://github.com/alexpviju/Ecom_Backend.git
cd Ecom_Backend
```

### 2. Create and activate virtual environment
```bash
python -m venv venv
venv\Scripts\activate   # On Windows
source venv/bin/activate # On Mac/Linux
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Apply migrations
```bash
python manage.py migrate
```

### 5. Create a superuser
```bash
python manage.py createsuperuser
```

### 6. Run development server
```bash
python manage.py runserver
```

---

## 🔑 Environment Variables

Create a `.env` file in your project root:

```env
SECRET_KEY=your-django-secret-key
DEBUG=True
RAZORPAY_KEY_ID=your_razorpay_key
RAZORPAY_KEY_SECRET=your_razorpay_secret
```

---

## 📡 API Documentation

You can import the provided Postman collection  


### 🔹 Authentication
- `POST /api/token/` → Get JWT token  
- `POST /api/token/refresh/` → Refresh JWT  

### 🔹 Cart
- `GET /api/buying/cart/` → Fetch current user’s cart  
- `POST /api/buying/cart/items/` → Add product/variant to cart  
- `PUT /api/buying/cart/items/<id>/` → Update cart item quantity  
- `DELETE /api/buying/cart/items/<id>/` → Remove item  

### 🔹 Orders
- `POST /api/buying/order/create/` → Create Razorpay order  
- `POST /api/buying/order/verify/` → Verify payment  

---

## ✅ Testing with Postman

1. Open Postman  
2. Import `Ecom_postman.postman_collection`  
3. Authenticate with a valid user token  
4. Call endpoints in order:  
   - Add product/variant to cart  
   - View cart  
   - Create order  
   - Verify payment  

---

## 📌 Tech Stack

- Python 3.13  
- Django 5.2.6  
- Django REST Framework 3.15  
- Razorpay Python SDK  
- SQLite (dev) / Any SQL DB (prod)  

---
