# FastAPI Authentication and Role-Based Authorization System

A secure and modular authentication and authorization system built with **FastAPI**, using **OAuth2 + JWT tokens**, and role-based access control.

This project provides:
- User Signup and Login
- JWT-based Token Authentication
- Role-based access control (Admin, User, Auditor, etc.)
- Password hashing using Bcrypt
- Password Reset via email (Tokenized link)
- Streamlit frontend integration

---

![image](https://github.com/user-attachments/assets/b6ff976b-0c2a-4dc3-b621-28df9d18b425)

![image](https://github.com/user-attachments/assets/f3c6b117-e3e2-44e1-a36c-9bdc3b6faca3)

![image](https://github.com/user-attachments/assets/cac585f0-8de9-4537-8773-4556d53dea59)

![image](https://github.com/user-attachments/assets/185ae31a-5cbd-418d-adc0-67c87c68bde0)

## 📁 Project Structure

```bash
.
├── main.py                  # FastAPI app entry point
├── authen.py               # Authentication & Authorization logic
├── models.py               # Pydantic models (User, Token, etc.)
├── database.py             # Mock user storage and helper methods
├── utils.py                # Token utils, hashing, constants
├── streamlit_app.py        # Streamlit client for interacting with API
├── requirements.txt
└── README.md
```
---
### Features
Authentication
- OAuth2PasswordBearer for secure token extraction.
- JWT token creation with username and role.
- Passwords are hashed using bcrypt before storing.

Authorization
- Admin-only endpoints using require_admin
- Role-based endpoints using require_roles(["admin", "auditor"])
- Protected routes using Depends(get_current_active_user)

Password Reset
- Generate a tokenized reset link sent via email.
- Token is verified and used to allow password update.
- Reset password page is served via Streamlit frontend.
--- 
### API Endpoints
#### Authentication
| Method | Endpoint   | Description                       |
| ------ | ---------- | --------------------------------- |
| POST   | `/token`   | Login with username and password  |
| POST   | `/signup`  | Register a new user               |
| GET    | `/profile` | Get current user info (Auth req.) |

#### Admin / Role-based Routes
| Method | Endpoint           | Access Role    | Description           |
| ------ | ------------------ | -------------- | --------------------- |
| GET    | `/admin/dashboard` | Admin          | Admin dashboard route |
| GET    | `/reports`         | Admin, Auditor | Access reports data   |


#### Password Reset
| Method | Endpoint           | Description                            |
| ------ | ------------------ | -------------------------------------- |
| POST   | `/forgot-password` | Send email with password reset token   |
| GET    | `/reset-password`  | Redirect to reset form (via Streamlit) |
| POST   | `/reset-password`  | Submit new password with token         |
--- 
#### Token Structure
JWT Token Payload:
```bash

{
  "sub": "username",
  "role": "admin",
  "exp": 1234567890
}
```
--- 
## How to Run the Application

Follow these steps to get the authentication & authorization system running locally on your machine:

### 1. Clone the Repository

```bash
git clone https://github.com/username/API-Authentication.git
cd API-Authentication
```

---

### 2. Create and Activate a Virtual Environment

```bash
# Create a virtual environment
python -m venv auth_env

# Activate it (Linux/macOS)
source auth_env/bin/activate

# Activate it (Windows)
auth_env\Scripts\activate
```

---

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

Make sure `pip` is updated:

```bash
pip install --upgrade pip
```

---

### 4. Create a `.env` File

Create a `.env` file in the root directory and add the following:

```env
SECRET_KEY=your-secret-key
ALGORITHM=HS256
RESET_PASSWORD_SALT=reset-password-salt
SMTP_EMAIL=your-email@gmail.com
SMTP_PASSKEY=your-app-password
API_BASE=http://127.0.0.1:8000
```

> 📌 Make sure to use a [Gmail App Password](https://support.google.com/accounts/answer/185833) for SMTP if using Gmail.

---

### 5. Run the FastAPI Backend

```bash
uvicorn main:app --reload
```

This starts the API server at:
`http://127.0.0.1:8000`

You can explore the API docs here:
`http://127.0.0.1:8000/docs`

---

### 6. Run the Streamlit Frontend

In a **new terminal**, activate your environment and run:

```bash
streamlit run streamlit_app.py
```

This opens the Streamlit UI in your browser at:
`http://localhost:8501`

---

### 🔐 Login & Try the Features

* Sign up as a new user
* Login to access your profile
* Try role-based routes like admin or report views (use dummy roles like `admin`, `auditor`)
* Use "Forgot Password" to send a reset link
---

## Future Improvements

* Add database integration (PostgreSQL or SQLite)
* OAuth with Single Sign On (SSO)
* Logging & Audit Trail
* Multi-Factor Authentication (MFA)
---


