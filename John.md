## models

### Updated Models in Detail

#### **1. Base Model (`base_model.py`)**

- **Purpose**: Provide shared attributes and methods for all models.
- **Attributes**:
  - `id`: Unique identifier for each record.
  - `created_at`: Timestamp of creation.
  - `updated_at`: Timestamp of the last update.
- **Methods**:
  - `save()`: Update the `updated_at` timestamp and persist changes.
  - `delete()`: Remove the record from the database.

---

#### **2. User Model (`user.py`)**

- **Purpose**: Manage user data and authentication.
- **Attributes**:
  - `username`: User's name.
  - `email`: Email address.
  - `password_hash`: Hashed password.
  - `role`: Role (e.g., customer, admin).
- **Methods**:
  - `check_password(password)`: Validate password.

---

#### **3. Restaurant Model (`restaurant.py`)**

- **Purpose**: Store restaurant details.
- **Attributes**:
  - `name`: Name of the restaurant.
  - `location`: Address or coordinates.
  - `cuisine_type`: Type of cuisine served.
  - `owner_id`: Foreign key linking to the user who owns the restaurant.
- **Methods**:
  - `get_menu()`: Retrieve menu items.

---

#### **4. Menu Item Model (`menu_item.py`)**

- **Purpose**: Store menu items for restaurants.
- **Attributes**:
  - `restaurant_id`: Foreign key linking to the restaurant.
  - `name`: Name of the menu item.
  - `description`: Description of the item.
  - `price`: Price.
  - `availability`: Boolean flag for availability.
- **Methods**:
  - `update_availability(status)`: Change availability.

---

#### **5. Order Model (`order.py`)**

- **Purpose**: Manage orders placed by users.
- **Attributes**:
  - `user_id`: Foreign key linking to the user.
  - `restaurant_id`: Foreign key linking to the restaurant.
  - `items`: List of menu items in the order.
  - `total_price`: Total cost.
  - `status`: Current status (e.g., pending, completed).
  - `payment_details`: Dictionary containing payment-related fields:
    - `amount`: Payment amount.
    - `payment_method`: Fixed as "PayPal".
    - `status`: Payment status (e.g., pending, completed).
- **Methods**:
  - `calculate_total()`: Compute the total price.
  - `process_payment()`: Handle payment logic.

---

#### **6. Review Model (`review.py`)**

- **Purpose**: Handle user feedback for restaurants.
- **Attributes**:
  - `user_id`: Foreign key linking to the user.
  - `restaurant_id`: Foreign key linking to the restaurant.
  - `rating`: Numeric rating (e.g., 1-5).
  - `comment`: User's comment.
- **Methods**:
  - `get_average_rating()`: Calculate average rating for a restaurant.

---

### Key Considerations

1. **Database Optimization**:
   - Establish relationships between tables using foreign keys.
   - Use indexing for frequently queried fields.
2. **Scalability**:
   - Modularized routes and models for easier maintenance.
3. **Security**:
   - Use hashed passwords with tools like `bcrypt`.
   - Sanitize user inputs to prevent SQL injection.
4. **Localization**:
   - Use `Flask-Babel` for multi-language support.
