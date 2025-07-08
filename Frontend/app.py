import streamlit as st
import requests
from dotenv import load_dotenv
import os
import time
# from Logging.Logger import CustomLogger

# importing the custom logger 
# logger_instance = CustomLogger(logger_name='Streamlit App', dir_name="logs")
# logger = logger_instance.get_logger()
load_dotenv()
API_BASE = os.getenv('API_BASE')
# print(API_BASE)
if "page" not in st.session_state:
    st.session_state.page = "home"

# Override from URL if present (only if it’s still on "home")
query_params = st.experimental_get_query_params()
url_page = query_params.get("page", [None])[0]
# Only set page from URL if it hasn't been overridden already
if url_page and "page_from_url" not in st.session_state:
    st.session_state.page = url_page
    st.session_state.page_from_url = True  # prevent future overrides


def home():
    st.title("👋 Welcome to My App")
    
    st.write("This app is designed to help understand Authentication and Authorization process in APIs.")
    
    st.subheader("Key Features")
    st.markdown("""
    - Secure login and signup
    - View personalized dashboards (Role based access)
    - Manage your settings and preferences
    """)
    
    # Show login/signup if not logged in
    if "token" not in st.session_state:
        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("🔐 Login"):
                st.session_state.page = "login"
        with col2:
            if st.button("📝 Sign Up"):
                st.session_state.page = "signup"
    else:
        # Show logout if already logged in
        st.success(f"Welcome back, {st.session_state.profile_data.get('full_name', 'User')}!")

        if st.button("🚪 Logout"):
            st.session_state.clear()
            st.session_state.page = "home"
            st.rerun()

def login():
    st.markdown("## 🔐 Welcome to My App")

    st.markdown("### Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        # with st.spinner("Authenticating..."):
        placeholder = st.empty()
        placeholder.info("Authenticating...")
        response = requests.post(
            f"{API_BASE}/token",
            {
                "grant_type": "password",
                "username": username,
                "password": password,
                "scope": "",
                "client_id": "",
                "client_secret": ""
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"}
        )

        if response.status_code == 200:
            placeholder.success("Logged in successfully!")
            time.sleep(1)  # simulate delay

            token_response = response.json()
            get_response = requests.get(f"{API_BASE}/profile",
                        headers={"Authorization": f"Bearer {token_response['access_token']}"}
                        )
            if get_response.status_code == 200:
                #Save token and profile data to session state
                st.session_state.token = token_response['access_token']
                print(st.session_state.token)
                st.session_state.profile_data = get_response.json()
                st.session_state.page = "profile"
                st.rerun()
            else:
                st.error("Error Authenticating")

            # st.code(token)
        else:
            st.error("Invalid credentials.")
    # st.markdown("🔑 [Forgot Password?](#)", unsafe_allow_html=True)
    if st.button("Reset Password"):
        st.session_state.page = "forgot_password"
    st.markdown("---")
    st.markdown("Don't have an account?")
    if st.button("Create an account"):
        st.session_state.page = "signup"

def signup():
    st.markdown("## 📝 Create an Account")
    
    new_user = st.text_input("New Username")
    fullname = st.text_input("Full Name")
    emailId = st.text_input("Email")
    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm Password", type="password")

    if st.button("Sign Up"):
        placeholder = st.empty()
        placeholder.info("Signing In...")
        if new_password == confirm_password:
            payload = {"username": new_user, "hashed_password": new_password, "full_name":fullname, "email":emailId, "role":"user"}
            response = requests.post(f"{API_BASE}/signup", json=payload)
            if response.status_code == 200:
                placeholder.success("User created successfully. Please log in.")
                st.session_state.page = "login"
                st.rerun() # force navigation
            else:
                placeholder.error("Sign up failed!")
            
        else:
            placeholder.error("Passwords do not match.")

    st.markdown("Already have an account?")
    if st.button("Back to Login"):
        st.session_state.page = "login"

def forgot_password():
    st.title("🔐 Forgot Password")

    username = st.text_input("Enter your username")
    email = st.text_input("Enter your registered email")

    if st.button("Send Reset Link"):
        response = requests.post(
            f"{API_BASE}/forgot-password",
            json={"username":username,"email": email}
        )

        if response.status_code == 200:
            st.success("Reset link sent to your email. Please check your inbox.")
        else:
            st.error("Failed to send reset link. Please try again or check the email.")
    
    if st.button("⬅️ Back to Login"):
        st.session_state.page = "login"
        st.rerun()

def reset_password():
    query_params = st.experimental_get_query_params()
    page = query_params.get("page", [None])[0]
    token = query_params.get("token", [None])[0]

    st.title("🔐 Reset Your Password")

    if not token:
        st.error("Missing token. Please check your email link.")
        return

    new_password = st.text_input("Enter new password", type="password")
    confirm_password = st.text_input("Confirm new password", type="password")
    placeholder = st.empty()

    if st.button("Reset Password"):
        if new_password == confirm_password:
            with placeholder:
                st.info("Resetting password...")
            response = requests.post(
                f"{API_BASE}/reset-password",
                data={"token": token, "new_password": new_password},
                headers={"Content-Type": "application/x-www-form-urlencoded"}
            )
            # print(response)
            if response.status_code == 200:
                placeholder.success("✅ Password updated successfully!")
                time.sleep(1)
                st.session_state.page = "login"
                st.rerun() # force navigation
            else:
                placeholder.error("❌ Token invalid or expired.")
        else:
            placeholder.error("Passwords do not match.")

def profile():
    st.title("👤 User Profile")

    if "profile_data" not in st.session_state:
        st.error("No profile data found. Please log in.")
        return

    profile_data = st.session_state.profile_data
    
    # Display profile info
    st.write("### Welcome,", profile_data.get("full_name", "User"))
    st.write(f"**Username:** {profile_data.get('username')}")
    st.write(f"**Email:** {profile_data.get('email')}")
    st.write(f"**Role:** {profile_data.get('role')}")

    # Role-based options
    if profile_data.get('role') == "admin":
        if st.button("Go to Admin Dashboard"):
            st.session_state.page = "admin_dashboard"

    if profile_data.get('role') in ["admin", "auditor"]:
        if st.button("📊 View Reports"):
            st.session_state.page = "reports" 

    if st.button("Home"):
        st.session_state.page = "home"

    st.button("🚪 Logout", on_click=lambda: st.session_state.clear())

def show_admin_dashboard():
    st.header("Admin Dashboard")
    token = st.session_state.token
    response = requests.get(
        f"{API_BASE}/admin/dashboard",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        st.success(response.json()["msg"])
    else:
        st.error("Access denied.")

def show_reports():
    st.header("📊 Reports Page")
    token = st.session_state.token
    response = requests.get(
        f"{API_BASE}/reports",
        headers={"Authorization": f"Bearer {token}"}
    )
    if response.status_code == 200:
        st.info(response.json()["msg"])
    else:
        st.error("You are not authorized to view this.")


# Router
if st.session_state.page == "home":
    home()
elif st.session_state.page == "login":
    login()
elif st.session_state.page == "signup":
    signup()
elif st.session_state.page == "profile":
    profile()
elif st.session_state.page == "forgot_password":
    forgot_password()
elif st.session_state.page == "reset_password":
    reset_password()
elif st.session_state.page == "admin_dashboard":
    show_admin_dashboard()
elif st.session_state.page == "reports":
    show_reports()
