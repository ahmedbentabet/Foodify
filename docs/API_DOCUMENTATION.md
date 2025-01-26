# Foodify REST API Documentation v1.1

## Overview

This document details the REST API endpoints for the Foodify food delivery platform.

## Authentication

Most endpoints require authentication using Flask-Login session cookies.

### Authentication Flow

```http
POST /login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "P@ssw0rd123",
  "remember": true
}

Response:
Set-Cookie: session=<encrypted_session_token>
```

💡 **Future Enhancement**: JWT Authentication planned for v2.0

## Base URL

All API endpoints are prefixed with `/api/v1/`

## Rate Limiting

🔒 **Recommended**: 50 requests per minute per user

## Endpoint Summary

| Endpoint | Method | Description | Auth Required |
|----------|---------|-------------|---------------|
| `/cart/state` | GET | Get current cart state | Yes |
| `/cart/update` | POST | Update cart items | Yes |
| `/search` | GET | Search menu items | No |
| `/payment/totals` | GET | Get order totals | Yes |
| `/apply_coupon` | POST | Apply coupon code | Yes |
| `/location/save` | POST | Save delivery location | Yes |
| `/submit_review` | POST | Submit restaurant review | Yes |
| `/orders/add_item` | POST | Add or update items in cart | Yes |

## Detailed Endpoint Specifications

### Cart State `GET /api/v1/cart/state`

**Description**: Get current user's cart state including items and total price

**Authentication**: Session Cookie (Flask-Login)

**Success Response**:

```json
{
    "items": [
        {
            "menu_item_id": "uuid",
            "quantity": 2
        }
    ],
    "order": {
        "id": "uuid",
        "total_price": 24.99
    }
}
```

### Cart Update `POST /api/v1/cart/update`

**Description**: Add, remove, or update items in cart

**Parameters**:

```json
{
    "menu_item_id": "uuid",
    "action": "increase|decrease"
}
```

**Success Response**:

```json
{
    "success": true,
    "order": {
        "id": "uuid",
        "total_price": 24.99,
        "status": "active"
    },
    "item": {
        "id": "uuid",
        "quantity": 2
    }
}
```

### Search Meals `GET /api/v1/search`

**Description**: Search menu items with pagination and filtering

**Query Parameters**:

- query (string): Search term
- restaurant (string): Filter by restaurant name
- page (integer): Page number
- per_page (integer = 8): Items per page

**Success Response**:

```json
{
    "meals": [
        {
            "id": "uuid",
            "name": "Meal Name",
            "price": 12.99,
            "is_available": true,
            "restaurant_name": "Restaurant Name",
            "image_name": "image_url"
        }
    ],
    "total": 20
}
```

### Payment Totals `GET /api/v1/payment/totals`

**Description**: Get order totals including delivery fee

**Success Response**:

```json
{
    "success": true,
    "subtotal": "24.99",
    "delivery_fee": "5.00",
    "total": "29.99"
}
```

### Submit Review `POST /api/v1/submit_review`

**Description**: Submit restaurant review with rating

**Parameters**:

```json
{
    "restaurant_id": "uuid",
    "rating": 5,
    "feedback": "Review text"
}
```

**Validation**:

- Rating must be between 1-5
- All fields required

**Success Response**:

```json
{
    "success": true,
    "message": "Review submitted successfully"
}
```

### Location Management `POST /api/v1/location/save`

**Description**: Save user's delivery location and preferences

**Authentication**: Required

**Request**:

```json
{
  "lat": 34.0522,
  "lng": -118.2437,
  "address": "123 Main St",
  "phone": "+1234567890",
  "instructions": "Gate code 1234"
}
```

**Success Response**:

```json
{
  "success": true
}
```

### Order Management `POST /api/v1/orders/add_item`

**Description**: Add or update items in cart

**Request**:

```json
{
  "menu_item_id": "uuid",
  "quantity_change": 1
}
```

**Success Response**:

```json
{
  "status": "success",
  "order_id": "uuid",
  "item": {
    "id": "uuid",
    "name": "Item Name",
    "price": 12.99,
    "quantity": 1
  }
}
```

## Hybrid Endpoints ⚠️

The following endpoints serve both HTML and JSON responses:

| Endpoint | HTML Response | JSON Response |
|----------|--------------|---------------|
| `/payment` | Default view | Add `Accept: application/json` |
| `/order` | Default view | Add `?format=json` |

**Deprecation Notice**: Hybrid endpoints will be split in v2.0 (Q4 2024)

## Error Codes

| Code | Description |
|------|-------------|
| 400 | Bad Request - Invalid parameters |
| 401 | Unauthorized - Login required |
| 404 | Not Found - Resource unavailable |
| 500 | Internal Server Error |

## Error Response Examples

### 400 Bad Request

```json
{
  "error": "Invalid rating value: 6/5",
  "valid_range": "1-5",
  "request_example": {
    "restaurant_id": "uuid",
    "rating": 5,
    "feedback": "Great service!"
  }
}
```

### 401 Unauthorized

```json
{
  "error": "Authentication required",
  "login_url": "/login"
}
```

## Security Recommendations 🔒

1. Add CSRF protection to all POST endpoints
2. Implement request rate limiting
3. Add input validation for all parameters
4. Migrate to JWT authentication
5. Add request logging

## Security Implementation Guide 🔒

### CSRF Protection

```python
# App initialization
from flask_wtf.csrf import CSRFProtect
csrf = CSRFProtect(app)

# Client requests
headers = {
    "X-CSRFToken": document.cookie.match('csrf_token=(.*?);')[1],
    "Content-Type": "application/json"
}
```

### Rate Limiting

```python
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["50 per minute"]
)
```

## Testing Utilities 🧪

### Postman Collection

**Click to expand:**

<details>
<summary>Postman Collection</summary>

```json
{
  "info": {
    "name": "Foodify API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Cart - Update",
      "request": {
        "method": "POST",
        "url": "{{base_url}}/api/v1/cart/update",
        "body": {
          "mode": "raw",
          "raw": "{\n  \"menu_item_id\": \"uuid\",\n  \"action\": \"increase\"\n}"
        }
      }
    }
  ]
}
```

</details>

### Complete Postman Collection

<details>
<summary>View Collection</summary>

```json
{
  "info": {
    "name": "Foodify API v1.1",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "Authentication",
      "item": [
        {
          "name": "Login",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/login",
            "body": {
              "mode": "raw",
              "raw": "{\"email\": \"user@example.com\", \"password\": \"password\"}"
            }
          }
        }
      ]
    },
    {
      "name": "Location",
      "item": [
        {
          "name": "Save Location",
          "request": {
            "method": "POST",
            "url": "{{base_url}}/api/v1/location/save",
            "body": {
              "mode": "raw",
              "raw": "{\"lat\": 34.0522, \"lng\": -118.2437, \"address\": \"123 Main St\"}"
            }
          }
        }
      ]
    }
  ]
}
```

</details>

### Curl Examples

```bash
# Login
curl -X POST http://localhost:5000/login \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password"}'

# Save Location
curl -X POST http://localhost:5000/api/v1/location/save \
  -H "Content-Type: application/json" \
  -H "Cookie: session=<your_session_cookie>" \
  -d '{"lat":34.0522,"lng":-118.2437,"address":"123 Main St"}'
```
