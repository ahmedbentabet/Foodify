# Foodify - Connecting Food Lovers with Restaurants

## Overview

Foodify is an innovative platform designed to connect food enthusiasts with their favorite restaurants. With features like detailed restaurant profiles, dynamic menus, online ordering, and user reviews, Foodify aims to make dining experiences more accessible and enjoyable. Built using a modular and scalable architecture, Foodify combines the power of Flask, PostgreSQL, and an intuitive web interface to deliver a seamless experience.

---

## Table of Contents

1. Features

2. Project Structure

3. Models Overview

4. Console

5. Setup Instructions

6. Usage

7. Technologies Used

8. Contributors

9. License

---

## Features

- **Restaurant Management**: Restaurants can create profiles, manage menus, and view customer reviews.

- **Menu Browsing**: Users can explore detailed menus, including descriptions, prices, and availability.

- **Ordering System**: Place orders directly from the platform and pay securely using PayPal.

- **User Reviews**: Customers can rate and review restaurants based on their experiences.

- **Interactive Console**: Administrators can manage the application via a command-line interface.

- **Localization**: Multi-language support for English, French, and Arabic using Flask-Babel.

---

## Project Structure

```plaintext
│── AUTHORS
├── README.md                  # Project description and instructions
├── console.py                 # Command-line interface for managing data

├── models/                    # Database models
│   ├── __init__.py            # Initialize models module
│   ├── base_model.py          # Base model with common fields
│   ├── user.py                # User model (handles authentication, profiles)
│   ├── restaurant.py          # Restaurant model (details about restaurants)
│   ├── menu_item.py           # Menu Item model (food items)
│   ├── order.py               # Order model (order details, status, and payment)
│   ├── review.py              # Review model (user feedback)
│   └── engine/                # PostgreSQL storage engine
│       ├── __init__.py
│       └── db_storage.py      # PostgreSQL connection and logic

├── tests/                     # Unit tests for modules
│   ├── test_models/           # Tests for models
│   └── test_web_flask/        # Tests for web routes

├── web_flask/                 # Web application using Flask
│   ├── __init__.py            # Initialize Flask app and configurations
│   ├── routes/                # Route files for scalable management
│   ├── static/                # Static assets (images, styles, scripts)
│   └── templates/             # HTML templates

└── translations/              # Flask-Babel translation files
    ├── en/                    # English translations
    ├── fr/                    # French translations
    └── ar/                    # Arabic translations
```

---

## Models Overview

### **1. Base Model**

- Common fields: `id`, `created_at`, `updated_at`.

- Methods: `save()`, `delete()`.

### **2. User Model**

- Fields: `username`, `email`, `password_hash`, `role`.

- Methods: `check_password(password)`.

### **3. Restaurant Model**

- Fields: `name`, `location`, `cuisine_type`, `owner_id`.

- Methods: `get_menu()`.

### **4. MenuItem Model**

- Fields: `restaurant_id`, `name`, `description`, `price`, `availability`.

- Methods: `update_availability(status)`.

### **5. Order Model**

- Fields: `user_id`, `restaurant_id`, `items`, `total_price`, `status`, `payment_status`, `payment_method`.

- Methods: `calculate_total()`.

### **6. Review Model**

- Fields: `user_id`, `restaurant_id`, `rating`, `comment`.

- Methods: `get_average_rating()`.

---

## Console

The interactive console provides a command-line interface for managing Foodify’s data. It supports CRUD operations for all models, searching, and listing records.

### Example Commands

- **Create a user:**

    ```bash
    create User username=JohnDoe email=john@example.com password=1234 role=customer
    ```

- **Read all restaurants:**

    ```bash
    read Restaurant
    ```

- **Update an order status:**

    ```bash
    update Order 1 status=completed
    ```

- **Delete a menu item:**

    ```bash
    delete MenuItem 5
    ```

---

## Setup Instructions

### **1. Clone the Repository**

```bash
git clone https://github.com/your-username/foodily.git
cd foodily
```

### **2. Install Dependencies**

Create and activate a virtual environment, then install required packages:

```bash
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
```

### **3. Set Up the Database**

- Configure your PostgreSQL database credentials in `models/engine/db_storage.py`.

- Initialize the database:

    ```bash
    python console.py
    (foodify) setup_db
    ```

### **4. Run the Application**

Start the Flask development server:

```bash
python web_flask/__init__.py
```

Access the application at `http://127.0.0.1:5000`.

---

## Usage

- **Web Application**: Interact with the platform via the browser.

- **Console**: Use `console.py` to manage data.

---

## Technologies Used

- **Backend**: Flask (Python)

- **Database**: PostgreSQL

- **Frontend**: HTML, CSS, JavaScript

- **Payment Integration**: PayPal

- **Localization**: Flask-Babel

- **Testing**: Unittest, Pytest

---

## Contributors

- **Tariq Omer** - Backend Developer

- **Ahmed** - Backend Developer

- **Abubakar** - Frontend Developer

- **John** - Database Administrator

---

## License

This project is licensed under the MIT License. See the LICENSE file for more details.
