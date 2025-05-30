import os
import json
import re
import hashlib
import secrets
import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
import google.generativeai as genai
import nltk
import warnings
from PIL import Image
import base64
from io import BytesIO
from datetime import datetime, timedelta

# Suppress NLTK download messages
nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)

# Suppress warnings if needed
warnings.filterwarnings('ignore')
from htmlTemplates import css, bot_template, user_template

# Load environment variables from .env file
load_dotenv()

# File to store user credentials
USER_DB_FILE = "user_database.json"

def img_to_base64(image):
    """Convert image to base64 for HTML display"""
    buffered = BytesIO()
    image.save(buffered, format="PNG")
    return base64.b64encode(buffered.getvalue()).decode()

def hash_password(password, salt=None):
    """Hash password using SHA-256 with salt"""
    if salt is None:
        salt = secrets.token_hex(16)
    pwdhash = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), 
                                  salt.encode('utf-8'), 100000)
    return salt + ":" + pwdhash.hex()

def verify_password(stored_password, provided_password):
    """Verify password against stored hash"""
    salt, stored_hash = stored_password.split(':')
    pwdhash = hashlib.pbkdf2_hmac('sha256', provided_password.encode('utf-8'), 
                                  salt.encode('utf-8'), 100000)
    return pwdhash.hex() == stored_hash

def load_user_database():
    """Load user database from file"""
    if os.path.exists(USER_DB_FILE):
        with open(USER_DB_FILE, 'r') as f:
            return json.load(f)
    return {"users": {}}

def save_user_database(db):
    """Save user database to file"""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(db, f, indent=4)

def is_valid_email(email):
    """Check if email is valid using regex pattern"""
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return bool(re.match(pattern, email))

def is_strong_password(password):
    """Check if password meets strength requirements"""
    # At least 8 characters, 1 uppercase, 1 lowercase, 1 digit, 1 special character
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'[0-9]', password):
        return False, "Password must contain at least one digit"
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        return False, "Password must contain at least one special character"
    
    return True, "Password is strong"

def login_page():
    """Display login page with enhanced UI."""
    # Load the image
    try:
        img = Image.open("hi.png")
    except:
        img = None
    
    st.markdown(
        """
        <style>
        .login-container {
            max-width: 500px;
            margin: 2rem auto;
            padding: 2.5rem;
            background: linear-gradient(135deg, #6e8efb, #a777e3);
            border-radius: 15px;
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.2);
            color: white;
        }
        .login-header {
            text-align: center;
            margin-bottom: 2rem;
        }
        .login-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            background: linear-gradient(to right, #ffffff, #e0e0e0);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
        .login-header p {
            font-size: 1.1rem;
            opacity: 0.9;
        }
        .stButton button {
            background: linear-gradient(to right, #4facfe 0%, #00f2fe 100%);
            color: white;
            width: 100%;
            padding: 0.75rem;
            border: none;
            border-radius: 25px;
            font-size: 1rem;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            margin-top: 1.5rem;
        }
        .stButton button:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.2);
        }
        .stTextInput input {
            border-radius: 25px;
            padding: 0.75rem 1rem;
            border: none;
            margin-bottom: 1rem;
        }
        .logo-container {
            display: flex;
            justify-content: center;
            margin-bottom: 1.5rem;
        }
        .logo-img {
            border-radius: 50%;
            width: 120px;
            height: 120px;
            object-fit: cover;
            border: 3px solid white;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.1);
        }
        .footer {
            text-align: center;
            margin-top: 1.5rem;
            font-size: 0.9rem;
            opacity: 0.8;
        }
        .toggle-link {
            text-align: center;
            margin-top: 1rem;
            color: white;
            text-decoration: underline;
            cursor: pointer;
        }
        .form-tabs {
            display: flex;
            justify-content: center;
            margin-bottom: 1.5rem;
        }
        .form-tab {
            padding: 0.5rem 1.5rem;
            border-radius: 25px;
            cursor: pointer;
            text-align: center;
            transition: all 0.3s ease;
            margin: 0 0.5rem;
        }
        .active-tab {
            background: rgba(255, 255, 255, 0.2);
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.1);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="login-container">', unsafe_allow_html=True)
    
    # Add logo/image if available
    if img:
        st.markdown(
            f'<div class="logo-container"><img src="data:image/png;base64,{img_to_base64(img)}" class="logo-img"></div>',
            unsafe_allow_html=True
        )
    
    st.markdown(
        '<div class="login-header">'
        '<h1>Welcome to Book Bot Insight</h1>'
        '<p>Your intelligent PDF companion for extracting knowledge</p>'
        '</div>',
        unsafe_allow_html=True
    )
    
    # Tab selection
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    
    with tab1:
        email = st.text_input("Email", placeholder="Enter your email", key="login_email")
        password = st.text_input("Password", type="password", placeholder="Enter your password", key="login_password")
        
        if st.button("Login", key="login_button"):
            if not email or not password:
                st.error("Please enter both email and password")
                return
            
            # Load user database
            user_db = load_user_database()
            
            # Check if user exists
            if email not in user_db["users"]:
                st.error("Email not found. Please sign up first.")
                return
            
            # Verify password
            if not verify_password(user_db["users"][email]["password"], password):
                st.error("Incorrect password. Please try again.")
                return
            
            # Set session state
            st.session_state['authenticated'] = True
            st.session_state['username'] = user_db["users"][email]["username"]
            st.session_state['email'] = email
            st.session_state['last_activity'] = datetime.now().isoformat()
            
            # Update last login time
            user_db["users"][email]["last_login"] = datetime.now().isoformat()
            save_user_database(user_db)
            
            st.success("Login successful!")
            st.rerun()
            
    with tab2:
        username = st.text_input("Username", placeholder="Choose a username", key="signup_username")
        email = st.text_input("Email", placeholder="Enter your email", key="signup_email")
        password = st.text_input("Password", type="password", placeholder="Create a password", key="signup_password")
        confirm_password = st.text_input("Confirm Password", type="password", placeholder="Confirm your password", key="confirm_password")
        
        # Password strength meter
        if password:
            is_strong, message = is_strong_password(password)
            if is_strong:
                st.success(message)
            else:
                st.warning(message)
        
        if st.button("Sign Up", key="signup_button"):
            # Validate inputs
            if not username or not email or not password or not confirm_password:
                st.error("All fields are required")
                return
            
            if not is_valid_email(email):
                st.error("Please enter a valid email address")
                return
            
            is_strong, message = is_strong_password(password)
            if not is_strong:
                st.error(message)
                return
            
            if password != confirm_password:
                st.error("Passwords do not match")
                return
            
            # Load user database
            user_db = load_user_database()
            
            # Check if email already exists
            if email in user_db["users"]:
                st.error("Email already registered. Please use a different email.")
                return
            
            # Create new user
            user_db["users"][email] = {
                "username": username,
                "password": hash_password(password),
                "created_at": datetime.now().isoformat(),
                "last_login": datetime.now().isoformat()
            }
            
            # Save user database
            save_user_database(user_db)
            
            st.success("Account created successfully! Please login.")
    
    st.markdown('</div>', unsafe_allow_html=True)

def check_session_timeout():
    """Check if session has timed out due to inactivity"""
    if 'last_activity' in st.session_state:
        last_activity = datetime.fromisoformat(st.session_state['last_activity'])
        if datetime.now() - last_activity > timedelta(minutes=30):  # 30 minute timeout
            st.warning("Your session has expired due to inactivity. Please login again.")
            st.session_state.clear()
            st.rerun()
        else:
            st.session_state['last_activity'] = datetime.now().isoformat()

def initialize_session_state():
    """Initialize session state variables."""
    for key in ['authenticated', 'chat_history', 'username', 'email', 'gemini_model', 'pdf_text', 'last_activity']:
        if key not in st.session_state:
            st.session_state[key] = None if key == 'gemini_model' else '' if key in ['username', 'email', 'last_activity'] else []

def get_api_key():
    """Retrieve API key from environment variables."""
    api_key = os.getenv("GOOGLE_GEMINI_KEY")
    if not api_key:
        st.error("Google Gemini API key not found. Set GOOGLE_GEMINI_KEY in environment variables.")
    return api_key

def initialize_gemini_model(api_key):
    """Initialize the Google Gemini model."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(model_name="gemini-2.0-flash")
        return model
    except Exception as e:
        st.error(f"Error initializing Gemini model: {str(e)}")
        return None

def generate_gemini_response(model, prompt):
    """Generate a response using Google Gemini."""
    try:
        response = model.generate_content(prompt)
        return response.text if response else ""
    except Exception as e:
        st.error(f"Error generating Gemini response: {str(e)}")
        return ""

def extract_pdf_text(pdf_docs):
    """Extract text from uploaded PDFs."""
    text = ""
    for pdf in pdf_docs:
        try:
            pdf_reader = PdfReader(pdf)
            for page in pdf_reader.pages:
                text += page.extract_text() or ""
        except Exception as e:
            st.error(f"Error reading PDF {pdf.name}: {str(e)}")
    return text.strip()

def process_user_input(user_question):
    """Handle user queries and display chat history."""
    # Update last activity time
    st.session_state['last_activity'] = datetime.now().isoformat()
    
    if not st.session_state.get("gemini_model"):
        api_key = get_api_key()
        if not api_key:
            return
        st.session_state['gemini_model'] = initialize_gemini_model(api_key)
    
    if st.session_state['gemini_model']:
        prompt = f"""
        You are an AI assistant designed to answer user questions. If the information is not found in the provided context, provide a general answer based on your knowledge.

        PDF Content:
        {st.session_state['pdf_text']}

        User Question:
        {user_question}
        """
        
        gemini_response = generate_gemini_response(st.session_state['gemini_model'], prompt)
        if gemini_response:
            st.session_state['chat_history'].append({"user": user_question, "bot": gemini_response})
            
            # Display chat history
            for chat in reversed(st.session_state['chat_history']):
                st.write(user_template.replace("{{MSG}}", chat["user"]), unsafe_allow_html=True)
                st.write(bot_template.replace("{{MSG}}", chat["bot"]), unsafe_allow_html=True)
        else:
            st.error("Failed to generate a response.")
    else:
        st.error("Gemini model is not initialized.")

def account_settings():
    """Display account settings page"""
    st.subheader("Account Settings")
    
    user_db = load_user_database()
    email = st.session_state['email']
    user_data = user_db["users"][email]
    
    st.markdown(f"**Username:** {user_data['username']}")
    st.markdown(f"**Email:** {email}")
    st.markdown(f"**Account Created:** {datetime.fromisoformat(user_data['created_at']).strftime('%Y-%m-%d')}")
    st.markdown(f"**Last Login:** {datetime.fromisoformat(user_data['last_login']).strftime('%Y-%m-%d %H:%M')}")
    
    st.markdown("---")
    
    st.subheader("Change Password")
    current_password = st.text_input("Current Password", type="password", key="current_password")
    new_password = st.text_input("New Password", type="password", key="new_password")
    confirm_new_password = st.text_input("Confirm New Password", type="password", key="confirm_new_password")
    
    if new_password:
        is_strong, message = is_strong_password(new_password)
        if is_strong:
            st.success(message)
        else:
            st.warning(message)
    
    if st.button("Update Password"):
        if not current_password or not new_password or not confirm_new_password:
            st.error("All fields are required")
            return
        
        if not verify_password(user_data["password"], current_password):
            st.error("Current password is incorrect")
            return
        
        is_strong, message = is_strong_password(new_password)
        if not is_strong:
            st.error(message)
            return
        
        if new_password != confirm_new_password:
            st.error("New passwords do not match")
            return
        
        # Update password
        user_db["users"][email]["password"] = hash_password(new_password)
        save_user_database(user_db)
        
        st.success("Password updated successfully!")

def main():
    """Main Streamlit app function."""
    st.set_page_config(
        page_title="Book Bot Insight",
        page_icon="📚",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    st.write(css, unsafe_allow_html=True)
    
    initialize_session_state()

    if not st.session_state['authenticated']:
        login_page()
        return
    else:
        check_session_timeout()

    # Display main application
    st.header(f"📚 Book Bot Insight - Welcome {st.session_state['username']}")
    
    # Add logout button and navigation in the sidebar
    with st.sidebar:
        st.markdown(
            """
            <style>
            .sidebar-header {
                font-size: 1.5rem;
                font-weight: bold;
                margin-bottom: 1rem;
                color: #6e8efb;
            }
            </style>
            <div class="sidebar-header">Book Bot Insight</div>
            """,
            unsafe_allow_html=True
        )
        
        # Navigation
        page = st.radio("Navigation", ["Home", "Account Settings"])
        
        st.markdown("---")
        
        if st.button("🚪 Logout", key="logout_button"):
            st.session_state.clear()
            st.rerun()
    
    if page == "Account Settings":
        account_settings()
    else:  # Home page
        # Document uploader and processing
        with st.sidebar:
            st.subheader("Your Documents")
            pdf_docs = st.file_uploader(
                "Upload PDFs and click 'Process'",
                accept_multiple_files=True,
                type="pdf",
                key="pdf_uploader"
            )
            
            if st.button("⚙️ Process Documents", key="process_button"):
                if not pdf_docs:
                    st.error("Please upload at least one PDF file.")
                    return
                    
                with st.spinner("Processing..."):
                    raw_text = extract_pdf_text(pdf_docs)
                    if not raw_text:
                        st.error("No text extracted from uploaded PDFs.")
                        return
                    st.session_state['pdf_text'] = raw_text
                    st.success("Documents processed successfully!")
        
        # Main chat area
        user_question = st.chat_input("Ask a question about your documents...")
        if user_question:
            process_user_input(user_question)

if __name__ == '__main__':
    main()