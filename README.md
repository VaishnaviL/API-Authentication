# API-Authentication

## Flow

## Backend ->
signup() -> checks if username exits, adds new user -> redirects to login page after success
Login() -> verifies password and user , creates new access token -> redirects to profile page on success
forgot_password() -> takes username, email and sends a reset link to email
reset_password() -> resets the password to new, redirects to login page after reset
home() -> basic home page with singup and login options

