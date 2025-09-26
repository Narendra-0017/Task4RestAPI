from flask import Flask, request, jsonify
from datetime import datetime
import uuid

app = Flask(__name__)

# In-memory storage for users
users = {}
user_id_counter = 1

# Helper function to generate unique user ID
def generate_user_id():
    global user_id_counter
    user_id = user_id_counter
    user_id_counter += 1
    return user_id

# Helper function to validate user data
def validate_user_data(data, required_fields=None):
    if required_fields is None:
        required_fields = ['name', 'email']
    
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    
    # Basic email validation
    if 'email' in data and '@' not in data['email']:
        return False, "Invalid email format"
    
    return True, "Valid"

# GET /users - Retrieve all users
@app.route('/users', methods=['GET'])
def get_all_users():
    """Get all users"""
    return jsonify({
        'success': True,
        'count': len(users),
        'users': list(users.values())
    }), 200

# GET /users/<id> - Retrieve specific user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Get a specific user by ID"""
    if user_id not in users:
        return jsonify({
            'success': False,
            'message': f'User with ID {user_id} not found'
        }), 404
    
    return jsonify({
        'success': True,
        'user': users[user_id]
    }), 200

# POST /users - Create new user
@app.route('/users', methods=['POST'])
def create_user():
    """Create a new user"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        # Validate required fields
        is_valid, message = validate_user_data(data)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': message
            }), 400
        
        # Check if email already exists
        for user in users.values():
            if user['email'] == data['email']:
                return jsonify({
                    'success': False,
                    'message': 'Email already exists'
                }), 409
        
        # Create new user
        user_id = generate_user_id()
        new_user = {
            'id': user_id,
            'name': data['name'],
            'email': data['email'],
            'created_at': datetime.now().isoformat(),
            'updated_at': datetime.now().isoformat()
        }
        
        # Add optional fields if provided
        if 'age' in data:
            new_user['age'] = data['age']
        if 'phone' in data:
            new_user['phone'] = data['phone']
        
        users[user_id] = new_user
        
        return jsonify({
            'success': True,
            'message': 'User created successfully',
            'user': new_user
        }), 201
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error creating user: {str(e)}'
        }), 500

# PUT /users/<id> - Update existing user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    """Update an existing user"""
    try:
        if user_id not in users:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404
        
        data = request.get_json()
        if not data:
            return jsonify({
                'success': False,
                'message': 'No JSON data provided'
            }), 400
        
        # Check if email is being updated and if it already exists
        if 'email' in data:
            for uid, user in users.items():
                if uid != user_id and user['email'] == data['email']:
                    return jsonify({
                        'success': False,
                        'message': 'Email already exists'
                    }), 409
        
        # Update user data
        user = users[user_id]
        for key, value in data.items():
            if key in ['name', 'email', 'age', 'phone']:
                user[key] = value
        
        user['updated_at'] = datetime.now().isoformat()
        
        return jsonify({
            'success': True,
            'message': 'User updated successfully',
            'user': user
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error updating user: {str(e)}'
        }), 500

# DELETE /users/<id> - Delete user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Delete a user"""
    try:
        if user_id not in users:
            return jsonify({
                'success': False,
                'message': f'User with ID {user_id} not found'
            }), 404
        
        deleted_user = users.pop(user_id)
        
        return jsonify({
            'success': True,
            'message': 'User deleted successfully',
            'deleted_user': deleted_user
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Error deleting user: {str(e)}'
        }), 500

# GET / - API information
@app.route('/', methods=['GET'])
def api_info():
    """API information and available endpoints"""
    return jsonify({
        'message': 'User Management REST API',
        'version': '1.0.0',
        'endpoints': {
            'GET /': 'API information',
            'GET /users': 'Get all users',
            'GET /users/<id>': 'Get specific user',
            'POST /users': 'Create new user',
            'PUT /users/<id>': 'Update user',
            'DELETE /users/<id>': 'Delete user'
        },
        'example_usage': {
            'create_user': {
                'method': 'POST',
                'url': '/users',
                'body': {
                    'name': 'John Doe',
                    'email': 'john@example.com',
                    'age': 30,
                    'phone': '+1234567890'
                }
            }
        }
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        'success': False,
        'message': 'Method not allowed'
    }), 405

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

if __name__ == '__main__':
    print("Starting User Management REST API...")
    print("Available endpoints:")
    print("  GET    /           - API information")
    print("  GET    /users      - Get all users")
    print("  GET    /users/<id> - Get specific user")
    print("  POST   /users      - Create new user")
    print("  PUT    /users/<id> - Update user")
    print("  DELETE /users/<id> - Delete user")
    print("\nServer starting on http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)

