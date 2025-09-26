# User Management REST API

A Flask-based REST API for managing user data with full CRUD operations.

## Features

- **GET** `/users` - Retrieve all users
- **GET** `/users/<id>` - Retrieve specific user by ID
- **POST** `/users` - Create new user
- **PUT** `/users/<id>` - Update existing user
- **DELETE** `/users/<id>` - Delete user
- **GET** `/` - API information and documentation

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Run the Flask application:
```bash
python app.py
```

The API will be available at `http://localhost:5000`

## API Endpoints

### 1. Get API Information
```http
GET /
```

**Response:**
```json
{
  "message": "User Management REST API",
  "version": "1.0.0",
  "endpoints": {
    "GET /": "API information",
    "GET /users": "Get all users",
    "GET /users/<id>": "Get specific user",
    "POST /users": "Create new user",
    "PUT /users/<id>": "Update user",
    "DELETE /users/<id>": "Delete user"
  }
}
```

### 2. Get All Users
```http
GET /users
```

**Response:**
```json
{
  "success": true,
  "count": 2,
  "users": [
    {
      "id": 1,
      "name": "John Doe",
      "email": "john@example.com",
      "age": 30,
      "phone": "+1234567890",
      "created_at": "2024-01-15T10:30:00",
      "updated_at": "2024-01-15T10:30:00"
    }
  ]
}
```

### 3. Get Specific User
```http
GET /users/1
```

**Response:**
```json
{
  "success": true,
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "age": 30,
    "phone": "+1234567890",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T10:30:00"
  }
}
```

### 4. Create New User
```http
POST /users
Content-Type: application/json

{
  "name": "Jane Smith",
  "email": "jane@example.com",
  "age": 25,
  "phone": "+0987654321"
}
```

**Response:**
```json
{
  "success": true,
  "message": "User created successfully",
  "user": {
    "id": 2,
    "name": "Jane Smith",
    "email": "jane@example.com",
    "age": 25,
    "phone": "+0987654321",
    "created_at": "2024-01-15T11:00:00",
    "updated_at": "2024-01-15T11:00:00"
  }
}
```

### 5. Update User
```http
PUT /users/1
Content-Type: application/json

{
  "name": "John Updated",
  "age": 31
}
```

**Response:**
```json
{
  "success": true,
  "message": "User updated successfully",
  "user": {
    "id": 1,
    "name": "John Updated",
    "email": "john@example.com",
    "age": 31,
    "phone": "+1234567890",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T11:15:00"
  }
}
```

### 6. Delete User
```http
DELETE /users/1
```

**Response:**
```json
{
  "success": true,
  "message": "User deleted successfully",
  "deleted_user": {
    "id": 1,
    "name": "John Updated",
    "email": "john@example.com",
    "age": 31,
    "phone": "+1234567890",
    "created_at": "2024-01-15T10:30:00",
    "updated_at": "2024-01-15T11:15:00"
  }
}
```

## Testing with cURL

### Get all users:
```bash
curl -X GET http://localhost:5000/users
```

### Get specific user:
```bash
curl -X GET http://localhost:5000/users/1
```

### Create new user:
```bash
curl -X POST http://localhost:5000/users \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "age": 28,
    "phone": "+1122334455"
  }'
```

### Update user:
```bash
curl -X PUT http://localhost:5000/users/1 \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Updated",
    "age": 29
  }'
```

### Delete user:
```bash
curl -X DELETE http://localhost:5000/users/1
```

## Testing with Postman

1. **Import Collection**: Create a new collection in Postman
2. **Add Requests**: Create requests for each endpoint
3. **Set Headers**: For POST and PUT requests, set `Content-Type: application/json`
4. **Test Endpoints**: Use the provided examples above

## Error Handling

The API includes comprehensive error handling:

- **400 Bad Request**: Invalid JSON or missing required fields
- **404 Not Found**: User ID doesn't exist
- **409 Conflict**: Email already exists
- **405 Method Not Allowed**: Wrong HTTP method
- **500 Internal Server Error**: Server-side errors

## Data Validation

- **Required fields**: `name` and `email`
- **Email validation**: Basic email format checking
- **Unique email**: No duplicate emails allowed
- **Optional fields**: `age` and `phone`

## Response Format

All responses follow a consistent format:

**Success Response:**
```json
{
  "success": true,
  "message": "Operation successful",
  "data": { ... }
}
```

**Error Response:**
```json
{
  "success": false,
  "message": "Error description"
}
```

## Development

The application uses in-memory storage, so data is lost when the server restarts. For production use, consider integrating with a database like SQLite, PostgreSQL, or MongoDB.

## License

This project is open source and available under the MIT License.
