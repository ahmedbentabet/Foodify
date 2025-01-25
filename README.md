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
│— AUTHORS
├── README.md                   # Project description and instructions
├── console.py                  # Console-based interface for testing/admin tasks

├── models/                     # Database models
│   ├── __init__.py             # Initialize models module
│   ├── base_model.py           # Base model with common fields
│   ├── user.py                 # User model (handles authentication, profiles)
│   ├── restaurant.py           # Restaurant model (restaurant details)
│   ├── menu_item.py            # Menu item model (food details)
│   ├── order.py                # Order model (order details, status, payments)
│   ├── review.py               # Review model (user feedback)
│   └── engine/                 # MySQL storage engine
│       ├── __init__.py
│       └── db_storage.py       # MySQL connection logic

├── tests/                      # Unit tests for modules and routes
│   ├── __init__.py
│   ├── test_models/            # Tests for models
│   │   ├── __init__.py
│   │   ├── test_user.py
│   │   ├── test_base_model.py
│   │   ├── test_restaurant.py
│   │   ├── test_menu_item.py
│   │   ├── test_order.py
│   │   ├── test_review.py
│   │   └── test_engine/
│   │       ├── __init__.py
│   │       └── test_db_storage.py
│   ├── test_console/           # Tests for the console
│   │   ├── __init__.py
│   │   ├── test_create.py      # Test 'create' functionality
│   │   ├── test_show.py        # Test 'show' functionality
│   │   ├── test_update.py      # Test 'update' functionality
│   │   ├── test_delete.py      # Test 'delete' functionality
│   │   ├── test_list.py        # Test 'list' functionality
│   │   └── test_count.py       # Test 'count' functionality
│   └── test_web_flask/         # Tests for web routes
│       ├── test_welcome_page.py
│       ├── test_user_page.py
│       ├── test_login.py
│       ├── test_signup.py
│       ├── test_order.py
│       └── test_payment.py

├── web_flask/                  # Web application using Flask
│   ├── __init__.py             # Initialize Flask app
│   ├── routes/                 # Route files
│   │   ├── welcome.py
│   │   ├── user.py
│   │   ├── restaurant.py
│   │   ├── login.py
│   │   ├── signup.py
│   │   ├── order.py
│   │   └── api.py
│   ├── static/                 # Static files (CSS, JS, images)
│   │   ├── images/
│   │   ├── styles/
│   │   └── scripts/
│   └── templates/              # HTML templates for the UI
│       ├── base.html
│       ├── welcome.html
│       ├── user.html
│       ├── login.html
│       ├── signup.html
│       ├── order.html
│       └── restaurant.html

└── translations/               # Multi-language support
    ├── en/
    ├── fr/
    └── ar/

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


---




# Foodify 🍔

Foodify is a Flask-based app designed to help you discover and explore amazing food options near you using the TomTom API. Follow this guide to set up the project locally.

---

## 🛠️ Prerequisites

Make sure you have the following installed on your system:

- **Python 3.8+**
- **pip** (Python package manager)
- **MySQL** (or any other database compatible with the app)

---

## ⚙️ Setting Up the Environment Variables

The app requires environment variables for proper configuration. To get started:

1. **Create a `.env` file**  
    In the root directory of the project, create a `.env` file and copy the structure from the `.env.example` file:
    
    ```bash
    cp .env.example .env
    ```
    
2. **Populate the `.env` File**  
    Open the `.env` file and add the necessary values. Here’s an example:
    
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
    
3. **How to Generate a Flask Secret Key**
    
    The secret key is essential for securing sessions and preventing tampering. To generate one, use Python’s built-in secrets module:
    
    - Run the following command in your terminal:
        
        ```bash
        python -c "import secrets; print(secrets.token_hex(24))"
        ```
        
    - Copy the output and paste it as the value for `FLASK_SECRET_KEY` in your `.env` file.
4. **Obtain API Keys**
    
    - Sign up for the [TomTom API](https://developer.tomtom.com/) and generate an API key.
    - Replace `your_tomtom_api_key` in the `.env` file with your actual key.

---

## 📦 Installing Dependencies

1. Create a virtual environment:
    
    ```bash
    python -m venv venv
    ```
    
2. Activate the virtual environment:
    
    - On **Windows**:
        
        ```bash
        venv\Scripts\activate
        ```
        
    - On **Linux/Mac**:
        
        ```bash
        source venv/bin/activate
        ```
        
3. Install required Python packages:
    
    ```bash
    pip install -r requirements.txt
    ```
    

---

## 🗄️ Setting Up the Database

1. Ensure your MySQL server is running.
    
2. Create the `foodify_db` database:
    
    ```sql
    CREATE DATABASE foodify_db;
    ```
    
3. Update the `.env` file with your database credentials.
    

---

## 🚀 Running the App

1. Run the Flask application:
    
    ```bash
    python app.py
    ```
    
2. Open your browser and navigate to:
    
    ```
    http://127.0.0.1:5000
    ```
    

---

## 🧪 Testing

To test the application, ensure the app is running and use the appropriate routes for the API.

---

## 🐛 Troubleshooting

- **Issue**: `ModuleNotFoundError: No module named 'flask'`  
    **Solution**: Ensure you’ve activated the virtual environment and installed dependencies.
    
- **Issue**: Database connection errors  
    **Solution**: Double-check the credentials in your `.env` file and ensure your database is running.
    

---

## 🙌 Contribution

We welcome contributions! Please fork the repository, make changes, and create a pull request.
