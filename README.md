# 🔐 FastAPI Authentication and Role-Based Authorization System

A secure and modular authentication and authorization system built with **FastAPI**, using **OAuth2 + JWT tokens**, and role-based access control.

This project provides:
- User Signup and Login
- JWT-based Token Authentication
- Role-based access control (Admin, User, Auditor, etc.)
- Password hashing using Bcrypt
- Password Reset via email (Tokenized link)
- Streamlit frontend integration

---

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
