from fastapi import FastAPI, Depends, HTTPException, status, Request, Form
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.security import OAuth2PasswordRequestForm
from models import User, UserInDB,Token, EmailSchema
from utils import verify_password, create_access_token, get_password_hash, generate_reset_token, verify_reset_token
from utils import smtp_email, smtp_passkey, API_BASE
from database import get_user, save_user, update_user_password
from authen import get_current_active_user, require_admin, require_roles
import smtplib
from email.message import EmailMessage
from fastapi.middleware.cors import CORSMiddleware
from Logging.Logger import CustomLogger


# importing the custom logger 
logger_instance = CustomLogger(logger_name='FastAPI App', dir_name="logs")
logger = logger_instance.get_logger()

app = FastAPI()
# Add CORS middleware to the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace ["*"] with your list of allowed origins if needed
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT"],
    allow_headers=["*"],
)

# # receive user credentials from login page
@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        user = get_user(form_data.username)
        #print(type(user))
        #print(user)
        if not user or not verify_password(form_data.password, user.hashed_password):
            raise HTTPException(status_code=400, detail="Incorrect username or password")
        access_token = create_access_token(data={"sub": user.username, "role":user.role})
        return {"access_token": access_token, "token_type": "bearer"}
    except Exception as e:
        #print(e)
        logger.error(e,exc_info=True)
        raise HTTPException(status_code=500,detail="Error Loggin In")

# if user does not exists , allow user to signup, checks if user already exists
@app.post("/signup/")
async def signup(request_data:UserInDB):
    try:
        existing_user = get_user(request_data.username)
        # #print(existing_user)
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists") 

        hashed_password1 = get_password_hash(request_data.hashed_password)
        # #print(hashed_password)
        new_user = UserInDB(
                        username=request_data.username,
                        full_name=request_data.full_name,
                        email=request_data.email,
                        role="user",
                        hashed_password=hashed_password1
                        )

        save_user(new_user)
        return JSONResponse(content="SignUp Completed!", status_code=200)
    except Exception as e:
        #print("error ",e)
        logger.error(e,exc_info=True)
        raise HTTPException(status_code=500,detail="Error Completing Signup")

@app.post("/forgot-password")
def forgot_password(data: EmailSchema):
    email = data.email
    # Optional: check if user exists
    user = get_user(data.username)
    #print("here user",user)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    token = generate_reset_token(data) # sending both email and username to generate rest token
    send_reset_email(email, token)
    return JSONResponse(content="Reset Link Sent",status_code=200)

# Triggered when the user clicks the link in the password reset email. will not update anything , redirects user to streamlit page to entere new passwords
@app.get("/reset-password")
def show_reset_form(token: str):
    streamlit_url = f"http://192.168.1.39:8501/?page=reset_password&token={token}"
    return RedirectResponse(url=streamlit_url)

@app.post("/reset-password")
def reset_password(token: str = Form(...), #streamlit requests.post is sending data as application/x-www-form-urlencoded — not JSON. Form(...) is used to declare a form field in a FastAPI endpoint.
                    new_password: str = Form(...)):
    verified_data = verify_reset_token(token)
    if not verified_data:
        raise HTTPException(status_code=400, detail="Invalid or expired token")

    # Save new password to DB (hash it first!)
    update_user_password(verified_data, new_password)

    return {"message": "Password updated successfully."}

@app.get("/profile")
def read_users_profile(current_user: User = Depends(get_current_active_user)):
    user_data = {
        "username": current_user.username,
        "role": current_user.role,
        "email": current_user.email,
        # "message": f"Welcome back, {current_user.full_name}!",
    }
    return user_data

def send_reset_email(to_email: str, token: str):
    reset_link = f"{API_BASE}/reset-password?token={token}"

    msg = EmailMessage()
    msg['Subject'] = "Reset your password"
    msg['From'] = smtp_email
    msg['To'] = to_email
    msg.set_content(f"""
    Hi,

    We received a request to reset your password. Click the link below to reset it:
    
    {reset_link}

    If you did not request a password reset, please ignore this email.
    """)

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(smtp_email, smtp_passkey)
        smtp.send_message(msg)

@app.get("/admin/dashboard")
def get_admin_dashboard(user: User = Depends(require_admin)):
    return {"msg": f"Welcome Admin {user.username}"}

@app.get("/reports")
def get_reports(user: User = Depends(require_roles(["admin", "auditor"]))):
    return {"msg": f"Reports for {user.role}"}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app)