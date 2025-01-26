# Foodify Database Documentation

  

## Database Overview

Foodify uses MySQL 8.0 to store and manage data for the food delivery platform. The database (`foodify_db`) consists of multiple tables that handle users, restaurants, menu items, orders, and reviews.

  

## Entity Relationship Diagram

[![Entity-Relationship-Diagram.png](https://i.postimg.cc/qMRVLVmy/Entity-Relationship-Diagram.png)](https://postimg.cc/7bpWHcrZ)

## Table Descriptions

  

### Clients

Stores user information for customers.

  

| Column | Type | Description |

|--------|------|-------------|

| id | varchar(60) | Primary key |

| username | varchar(50) | User's display name |

| email | varchar(100) | Unique email address |

| password | varchar(128) | Hashed password |

| address | varchar(500) | Delivery address |

| latitude | float | Location coordinate |

| longitude | float | Location coordinate |

| delivery_instructions | varchar(500) | Special delivery notes |

| created_at | datetime | Record creation timestamp |

| updated_at | datetime | Record update timestamp |

  

### Restaurants

Stores restaurant information.

  

| Column | Type | Description |

|--------|------|-------------|

| id | varchar(60) | Primary key |

| name | varchar(100) | Restaurant name |

| city | varchar(100) | Restaurant location |

| logo_url | varchar(255) | Path to logo image |

| created_at | datetime | Record creation timestamp |

| updated_at | datetime | Record update timestamp |

  

### MenuItems

Stores food items available at restaurants.

  

| Column | Type | Description |

|--------|------|-------------|

| id | varchar(60) | Primary key |

| restaurant_id | varchar(60) | Foreign key to restaurants |

| name | varchar(100) | Item name |

| price | decimal(10,2) | Item price |

| is_available | tinyint(1) | Availability status |

| image_url | varchar(255) | Path to item image |

| created_at | datetime | Record creation timestamp |

| updated_at | datetime | Record update timestamp |

  

### Orders

Tracks customer orders.

  

| Column | Type | Description |

|--------|------|-------------|

| id | varchar(60) | Primary key |

| client_id | varchar(60) | Foreign key to clients |

| status | varchar(20) | Order status |

| order_date | datetime | Order placement time |

| total_price | decimal(10,2) | Total order amount |

| created_at | datetime | Record creation timestamp |

| updated_at | datetime | Record update timestamp |

  

### OrderItems

Links orders to menu items with quantities.

  

| Column | Type | Description |

|--------|------|-------------|

| id | varchar(60) | Primary key |

| order_id | varchar(60) | Foreign key to orders |

| menu_item_id | varchar(60) | Foreign key to menu_items |

| quantity | int | Number of items ordered |

| created_at | datetime | Record creation timestamp |

| updated_at | datetime | Record update timestamp |

  

### Reviews

Stores customer reviews for restaurants.

  

| Column | Type | Description |

|--------|------|-------------|

| id | varchar(60) | Primary key |

| client_id | varchar(60) | Foreign key to clients |

| restaurant_id | varchar(60) | Foreign key to restaurants |

| rating | int | Numerical rating |

| comment | text | Review text |

| created_at | datetime | Record creation timestamp |

| updated_at | datetime | Record update timestamp |

  

## Relationships

  

1. **Client -> Orders**: One-to-Many

   - A client can have multiple orders

   - Each order belongs to one client

  

2. **Restaurant -> MenuItems**: One-to-Many

   - A restaurant can have multiple menu items

   - Each menu item belongs to one restaurant

  

3. **Order -> OrderItems**: One-to-Many

   - An order can have multiple order items

   - Each order item belongs to one order

  

4. **MenuItem -> OrderItems**: One-to-Many

   - A menu item can be in multiple order items

   - Each order item references one menu item

  

5. **Client -> Reviews**: One-to-Many

   - A client can write multiple reviews

   - Each review belongs to one client

  

6. **Restaurant -> Reviews**: One-to-Many

   - A restaurant can have multiple reviews

   - Each review belongs to one restaurant

  

## Database Backup and Restore

  

### Creating a backup

```bash

mysqldump -u username -p foodify_db > foodify_backup.sql

```

  

### Restoring from backup

```bash

mysql -u username -p foodify_db < foodify_backup.sql

```

  

## Common Queries

  

### Get all menu items for a restaurant

```sql

SELECT * FROM menu_items

WHERE restaurant_id = 'restaurant_uuid';

```

  

### Get client's order history

```sql

SELECT o.*, oi.quantity, mi.name, mi.price

FROM orders o

JOIN order_items oi ON o.id = oi.order_id

JOIN menu_items mi ON oi.menu_item_id = mi.id

WHERE o.client_id = 'client_uuid';

```

  

### Get restaurant's average rating

```sql

SELECT restaurant_id, AVG(rating) as avg_rating

FROM reviews

GROUP BY restaurant_id;