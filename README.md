# Foodify 🍔

## Overview

Foodify is a Flask-based food delivery platform designed to help you discover and explore amazing food options near you using the TomTom API. Built with MySQL and Flask, it provides real-time order tracking, location-based delivery, secure user authentication, and a restaurant review system.

---

## Table of Contents

1. Features
2. Project Structure
3. Models Overview
4. Console
5. Setup Instructions
6. Usage
7. Technologies Used
8. Security Considerations
9. API Notes
10. Contributors
11. License

---

## ✅ Verified Features

- **Restaurant Management**: Browse and order from local restaurants
- **Client Model**: Manages key fields such as username, email, address, latitude, longitude, phone
- **Menu System**: Dynamic menu items with availability tracking
- **Order Processing**: Real-time order status and tracking
- **User Reviews**: Restaurant ratings and feedback system
- **Location Services**: TomTom API integration for delivery
- **Secure Authentication**: Session-based user management (transition to JWT planned for future)

---

## 📁 Project Structure

```plaintext
│— AUTHORS
├── README.md                   # Project description and instructions
├── console.py                  # Console-based interface for testing/admin tasks

├── models/                     # Database models
│   ├── __init__.py             # Initialize models module
│   ├── base_model.py           # Base model with common fields
│   ├── client.py               # Client model (corresponds to 'clients' table)
│   ├── restaurant.py           # Restaurant model (restaurant details)
│   ├── menu_item.py            # Menu item model (food details)
│   ├── order.py                # Order model (order details, status, payments)
│   ├── review.py               # Review model (user feedback)
│   └── engine/                 # MySQL storage engine
│       ├── __init__.py
│       └── db_storage.py       # MySQL connection logic

├── routes/                     # Route handlers
│   ├── __init__.py
│   ├── ...
│   └── config.py

├── docs/
│   ├── API_DOCUMENTATION.md
│   └── DATABASE_DOCUMENTATION.md

├── database/
│   └── foodify_backup.sql      # MySQL data dump

├── tests/                      # Unit tests for modules and routes
│   ├── __init__.py
│   ├── test_models/
│   │   ├── __init__.py
│   │   ├── test_client.py
│   │   └── ...
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variable template
├── .gitignore
├── app.py                      # Main Flask application entry point
└── LICENSE                     # License file (add or update as needed)
```

---

## 📊 Models Overview

- **Client** (`clients` table):
  - Fields: `id`, `username`, `email`, `password`, `address`, `latitude`, `longitude`, `phone`, `delivery_instructions`, `created_at`, `updated_at`
  - Handles authentication, profile data, and location info

- **Restaurant** (`restaurants` table):
  - Fields: `id`, `name`, `city`, `logo_url`, `created_at`, `updated_at`

- **MenuItem** (`menu_items` table):
  - Fields: `id`, `restaurant_id`, `name`, `price`, `is_available`, `image_url`, `created_at`, `updated_at`

- **Order** (`orders` table):
  - Fields: `id`, `client_id`, `status`, `order_date`, `total_price`, `created_at`, `updated_at`

- **OrderItem** (`order_items` table):
  - Fields: `id`, `order_id`, `menu_item_id`, `quantity`, `created_at`, `updated_at`

- **Review** (`reviews` table):
  - Fields: `id`, `client_id`, `restaurant_id`, `rating`, `comment`, `created_at`, `updated_at`

---

## 🎮 Console Commands

Use `console.py` for administrative or interactive tasks. It allows testing model queries, debugging, and direct database operations:

```bash
python console.py
```

---

## 🚀 Getting Started

### 🛠️ Prerequisites

Make sure you have the following installed:

- Python 3.8+
- pip (Python package manager)
- MySQL (or any other compatible database)

### ⚙️ Setting Up the Environment Variables

1.**Create a `.env` file**

```bash
cp .env.example .env
```

2.**Configure Environment Variables**

```env
# Flask
FLASK_SECRET_KEY=your_flask_secret_key

# Database
FOOD_MYSQL_USER=your_database_user
FOOD_MYSQL_PWD=your_database_password
FOOD_MYSQL_HOST=127.0.0.1
FOOD_MYSQL_DB=foodify_db

# TomTom API
TOMTOM_API_KEY=your_tomtom_api_key
```

3.**Generate Flask Secret Key**

```bash
python -c "import secrets; print(secrets.token_hex(24))"
```

4.**Obtain TomTom API Key**

- Sign up at [TomTom API](https://developer.tomtom.com/)
- Add your API key to `.env`

### 📦 Installation Steps

1. **Create and activate virtual environment**

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate     # Windows
```

2.**Install dependencies**

```bash
pip install -r requirements.txt
```

### 🗄️ Database Setup

1. **Create Database**

```sql
CREATE DATABASE foodify_db;
```

2.**Load Sample Data (Optional)**

```bash
mysql -u <username> -p foodify_db < database/foodify_backup.sql
```

Refer to [docs/DATABASE_DOCUMENTATION.md](docs/DATABASE_DOCUMENTATION.md) for schema details.

---

## 🔧 Usage & Development

- Register or log in to explore restaurants and place orders.
- Customize location data via the TomTom API (configure your `TOMTOM_API_KEY`).
- Modify code in `routes` for additional endpoints or logic.

---

## 🛡️ Security Considerations

- **CSRF Protection**: Enabled via Flask-WTF. Ensure `CSRFProtect(app)` is used in `app.py`.
- **Session-Based Login**: @login_required for protected routes.
- **Rate Limiting**: Recommended at 50 requests/min per user.
- **Future**: Transition to JWT-based authentication is planned; see `API_DOCUMENTATION.md` for details.

---

## 📚 API Documentation

- Refer to [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md) for detailed endpoint usage and examples.
- Hybrid endpoints (HTML + JSON) will be deprecated in favor of REST/JSON in v2.0.
- To enable TomTom location-based services, provide `TOMTOM_API_KEY` in your `.env`.

---

## 🐛 Troubleshooting

Common issues and solutions:

- **ModuleNotFoundError: No module named 'flask'**
  Ensure virtual environment is activated and dependencies are installed

- **Database Connection Errors**
  Verify credentials in `.env` and database server status

- **TomTom API Issues**
  Check API key validity and request limits

---

## 👥 Contributors

- **Tariq Omer** - Backend Developer
- **Ahmed** - Backend Developer
- **Abubakar** - Frontend Developer
- **John** - Database Administrator

---

## 📄 License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## 🤝 Contributing

We welcome contributions! Please:

1. Fork the repository
2. Create a feature branch
3. Submit a pull request

For detailed API documentation, see [docs/API_DOCUMENTATION.md](docs/API_DOCUMENTATION.md).
