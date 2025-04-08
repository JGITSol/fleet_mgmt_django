# Lynx JS Authentication API

This document provides information about the authentication API endpoints for the Lynx JS mobile application integration with the Car Fleet Management Django backend.

## Overview

The authentication API allows Lynx JS mobile applications to:

- Register new users
- Login existing users
- Validate authentication tokens
- Retrieve user profile information
- Logout users

All authentication is handled using token-based authentication, which is secure and works seamlessly across all platforms that Lynx supports.

## API Endpoints

### Register

**Endpoint:** `/api/auth/register/`

**Method:** POST

**Description:** Register a new user account

**Request Body:**
```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "secure_password",
  "password2": "secure_password"
}
```

**Response (201 Created):**
```json
{
  "user": {
    "id": 1,
    "username": "example_user",
    "email": "user@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Login

**Endpoint:** `/api/auth/login/`

**Method:** POST

**Description:** Authenticate a user and receive a token

**Request Body:**
```json
{
  "username": "example_user",
  "password": "secure_password"
}
```

**Response (200 OK):**
```json
{
  "user": {
    "id": 1,
    "username": "example_user",
    "email": "user@example.com",
    "first_name": "",
    "last_name": ""
  },
  "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b"
}
```

### Validate Token

**Endpoint:** `/api/auth/validate-token/`

**Method:** GET

**Description:** Check if a token is valid

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK):**
```json
{
  "is_valid": true,
  "user": {
    "id": 1,
    "username": "example_user",
    "email": "user@example.com",
    "first_name": "",
    "last_name": ""
  }
}
```

### User Profile

**Endpoint:** `/api/auth/profile/`

**Method:** GET

**Description:** Get the current user's profile information

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK):**
```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com",
  "first_name": "",
  "last_name": ""
}
```

### Logout

**Endpoint:** `/api/auth/logout/`

**Method:** POST

**Description:** Invalidate the current user's token

**Headers:**
```
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

**Response (200 OK):**
```json
{
  "message": "Successfully logged out."
}
```

## Integration with Lynx JS

See the `lynx_client_example.js` file for a complete example of how to integrate these authentication endpoints with a Lynx JS mobile application.

### Basic Usage

```javascript
// Import the authentication functions
import { login, register, logout, validateToken } from './api';

// Login a user
const loginUser = async (username, password) => {
  try {
    const response = await login(username, password);
    console.log('Logged in successfully:', response.user);
    return response;
  } catch (error) {
    console.error('Login failed:', error);
  }
};

// Check if a token is valid
const checkAuth = async () => {
  try {
    const { isValid, user } = await validateToken();
    if (isValid) {
      console.log('Token is valid, user:', user);
      return user;
    } else {
      console.log('Token is invalid or expired');
      return null;
    }
  } catch (error) {
    console.error('Token validation failed:', error);
    return null;
  }
};
```

## Security Considerations

1. Always use HTTPS in production environments
2. Store tokens securely in the Lynx app's local storage
3. Implement token expiration and refresh mechanisms for long-lived applications
4. Restrict CORS settings in production to only allow requests from trusted domains

## Troubleshooting

- If you receive a 401 Unauthorized error, your token may be invalid or expired
- If you receive a 400 Bad Request error, check your request payload for missing or invalid fields
- For CORS issues, ensure the Django backend has proper CORS settings configured