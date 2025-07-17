import streamlit as st
import pandas as pd
import hashlib
import uuid
from datetime import datetime
import os

def initialize_auth():
    """Initialize authentication system with proper session state management"""
    # Initialize all authentication-related session state variables
    if 'authenticated' not in st.session_state:
        st.session_state.authenticated = False
    
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None
    
    if 'username' not in st.session_state:
        st.session_state.username = None
    
    if 'is_admin' not in st.session_state:
        st.session_state.is_admin = False

def safe_read_csv(file_path, default_columns):
    """Safely read CSV file with fallback to empty DataFrame"""
    try:
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            return pd.read_csv(file_path)
        else:
            return pd.DataFrame(columns=default_columns)
    except (pd.errors.EmptyDataError, pd.errors.ParserError):
        return pd.DataFrame(columns=default_columns)

def hash_password(password):
    """Hash password for storage"""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from CSV file"""
    default_columns = ['user_id', 'username', 'email', 'password_hash', 'is_admin', 'created_at']
    return safe_read_csv('data/users.csv', default_columns)

def save_user(username, email, password, is_admin=False):
    """Save new user to CSV"""
    users_df = load_users()
    
    user_id = str(uuid.uuid4())
    new_user = {
        'user_id': user_id,
        'username': username,
        'email': email,
        'password_hash': hash_password(password),
        'is_admin': is_admin,
        'created_at': datetime.now().isoformat()
    }
    
    users_df = pd.concat([users_df, pd.DataFrame([new_user])], ignore_index=True)
    users_df.to_csv('data/users.csv', index=False)
    return user_id

def authenticate_user(username, password):
    """Authenticate user credentials"""
    users_df = load_users()
    
    if not users_df.empty:
        user_row = users_df[users_df['username'] == username]
        if not user_row.empty:
            stored_hash = user_row.iloc[0]['password_hash']
            if stored_hash == hash_password(password):
                return user_row.iloc[0].to_dict()
    return None

def check_authentication():
    """Check if user is authenticated, show login if not"""
    # Ensure session state is initialized
    initialize_auth()
    
    if st.session_state.authenticated:
        return True
    
    # Show login interface
    st.title("🏏 VPL Fantasy League")
    st.subheader("TURF 32 Premier League Season 3")
    st.markdown("Please login to continue")
    
    tab1, tab2, tab3 = st.tabs(["🔐 Login", "👤 Register", "👨‍💼 Admin"])
    
    with tab1:
        with st.form("login_form"):
            st.subheader("User Login")
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                user = authenticate_user(username, password)
                if user:
                    st.session_state.authenticated = True
                    st.session_state.user_id = user['user_id']
                    st.session_state.username = user['username']
                    st.session_state.is_admin = user['is_admin']
                    st.success("Login successful!")
                    st.rerun()
                else:
                    st.error("Invalid credentials")
    
    with tab2:
        with st.form("register_form"):
            st.subheader("Create Account")
            reg_username = st.text_input("Choose Username")
            reg_email = st.text_input("Email")
            reg_password = st.text_input("Password", type="password")
            reg_confirm = st.text_input("Confirm Password", type="password")
            register = st.form_submit_button("Register")
            
            if register:
                if reg_password == reg_confirm:
                    users_df = load_users()
                    if users_df.empty or reg_username not in users_df['username'].values:
                        user_id = save_user(reg_username, reg_email, reg_password)
                        st.success("Account created successfully! Please login.")
                    else:
                        st.error("Username already exists")
                else:
                    st.error("Passwords don't match")
    
    with tab3:
        with st.form("admin_form"):
            st.subheader("Admin Login")
            admin_username = st.text_input("Admin Username")
            admin_password = st.text_input("Admin Password", type="password")
            admin_login = st.form_submit_button("Admin Login")
            
            if admin_login:
                # Check default admin credentials
                if admin_username == "admin" and admin_password == "vpl2024":
                    st.session_state.authenticated = True
                    st.session_state.user_id = "admin"
                    st.session_state.username = "Administrator"
                    st.session_state.is_admin = True
                    st.success("Admin login successful!")
                    st.rerun()
                else:
                    # Check database admin users
                    user = authenticate_user(admin_username, admin_password)
                    if user and user['is_admin']:
                        st.session_state.authenticated = True
                        st.session_state.user_id = user['user_id']
                        st.session_state.username = user['username']
                        st.session_state.is_admin = True
                        st.success("Admin login successful!")
                        st.rerun()
                    else:
                        st.error("Invalid admin credentials")
    
    return False

def logout():
    """Logout current user"""
    # Clear session state
    st.session_state.authenticated = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.is_admin = False
    
    # Force page reload to show login screen
    st.rerun()

def get_current_user():
    """Get current user information safely"""
    initialize_auth()
    
    if st.session_state.authenticated:
        return {
            'user_id': st.session_state.user_id,
            'username': st.session_state.username,
            'is_admin': st.session_state.is_admin
        }
    return None