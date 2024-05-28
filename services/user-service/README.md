
# Healthcare Management System


## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [API Endpoints](#api-endpoints)
  - [User Registration](#user-registration)
  - [User Login](#user-login)
  - [Get User Profile](#get-user-profile)
  - [Update User Profile](#update-user-profile)
  - [Request Password Reset](#request-password-reset)
  - [Reset Password](#reset-password)
  - [Send Verification Email](#send-verification-email)
  - [Verify Email](#verify-email)
  - [Admin-Only Endpoint](#admin-only-endpoint)
  - [Setup Multi-Factor Authentication (MFA)](#setup-multi-factor-authentication-mfa)
- [Testing the Endpoints](#testing-the-endpoints)
- [License](#license)

## Features

- User Registration
- User Login
- User Profile Management
- Password Reset
- Email Verification
- Multi-Factor Authentication (MFA)
- Role-Based Access Control (RBAC)

## Prerequisites

- Python 3.8+
- MongoDB
- Flask
- Postman (for testing the API endpoints)

## Installation

1. **Clone the Repository**

   ```bash
   git clone https://github.com/your-username/healthcare-system.git
   cd healthcare-system
   ```

2. **Set Up Virtual Environment**

   ```bash
   python -m venv venv
   venv\Scripts\activate  # On Windows
   ```

3. **Install Dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Create a `.env` File**

   Create a `.env` file in the root of the project directory with the following content:

   ```env
   SECRET_KEY=your_secret_key
   MONGO_URI=mongodb://localhost:27017/healthcare
   JWT_SECRET=your_jwt_secret
   ```

5. **Ensure MongoDB is Running**

   Start the MongoDB server:

   ```bash
   mongod
   ```

## Running the Application

1. **Activate the Virtual Environment**

   ```bash
   venv\Scripts\activate  # On Windows
   ```

2. **Run the Flask Application**

   ```bash
   python run.py
   ```

3. **Access the Application**

   The application will be running at `http://127.0.0.1:5000`.

## API Endpoints

### User Registration

**Endpoint:** `POST /api/auth/register`  
**Headers:** `Content-Type: application/json`  
**Body:**

```json
{
  "username": "testuser",
  "password": "password123",
  "email": "testuser@example.com",
  "phone": "1234567890",
  "role": "patient"
}
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### User Login

**Endpoint:** `POST /api/auth/login`  
**Headers:** `Content-Type: application/json`  
**Body:**

```json
{
  "username": "testuser",
  "password": "password123"
}
```

**Response:**

```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

### Get User Profile

**Endpoint:** `GET /api/auth/profile`  
**Headers:** `Authorization: Bearer {token}`  

**Response:**

```json
{
  "username": "testuser",
  "email": "testuser@example.com",
  "phone": "1234567890",
  "role": "patient",
  "profile_picture": null,
  "mfa_enabled": false,
  "email_verified": false
}
```

### Update User Profile

**Endpoint:** `PUT /api/auth/profile`  
**Headers:** `Authorization: Bearer {token}`, `Content-Type: application/json`  
**Body:**

```json
{
  "email": "newemail@example.com",
  "phone": "0987654321",
  "profile_picture": "new_profile_picture_url"
}
```

**Response:**

```json
{
  "message": "Profile updated successfully"
}
```

### Request Password Reset

**Endpoint:** `POST /api/auth/request-reset-password`  
**Headers:** `Content-Type: application/json`  
**Body:**

```json
{
  "email": "testuser@example.com"
}
```

**Response:**

```json
{
  "message": "Password reset email sent"
}
```

### Reset Password

**Endpoint:** `POST /api/auth/reset-password`  
**Headers:** `Content-Type: application/json`  
**Body:**

```json
{
  "token": "reset_token_received_via_email",
  "new_password": "newpassword123"
}
```

**Response:**

```json
{
  "message": "Password has been reset successfully"
}
```

### Send Verification Email

**Endpoint:** `POST /api/auth/send-verification-email`  
**Headers:** `Content-Type: application/json`  
**Body:**

```json
{
  "email": "testuser@example.com"
}
```

**Response:**

```json
{
  "message": "Verification email sent"
}
```

### Verify Email

**Endpoint:** `GET /api/auth/verify-email`  
**Parameters:** `token=verification_token_received_via_email`  

**Response:**

```json
{
  "message": "Email has been verified successfully"
}
```

### Admin-Only Endpoint

**Endpoint:** `GET /api/auth/admin-only`  
**Headers:** `Authorization: Bearer {token}`  

**Response:**

```json
{
  "message": "Welcome, admin!"
}
```

### Setup Multi-Factor Authentication (MFA)

**Endpoint:** `POST /api/auth/setup-mfa`  
**Headers:** `Authorization: Bearer {token}`, `Content-Type: application/json`  
**Body:**

```json
{
  "mfa_enabled": true
}
```

**Response:**

```json
{
  "message": "MFA setting updated successfully"
}
```

## Testing the Endpoints

To test the endpoints, you can use Postman:

1. **Register a new user** by sending a POST request to `/api/auth/register`.
2. **Login with the user** by sending a POST request to `/api/auth/login` and obtain the JWT token.
3. **Access protected endpoints** by including the JWT token in the `Authorization` header as `Bearer {token}`.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
```

