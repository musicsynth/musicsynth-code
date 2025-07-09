import os
import streamlit as st
from supabase import create_client, Client
from dotenv import load_dotenv
import re
from typing import Optional, Dict, Any
from theme_manager import theme_manager

# Load environment variables
load_dotenv()

class SupabaseAuth:
    def __init__(self):
        # Initialize Supabase client
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_ANON_KEY")
        
        if not self.supabase_url or not self.supabase_key:
            st.error("Supabase configuration not found. Please check your environment variables.")
            st.stop()
        
        self.supabase: Client = create_client(self.supabase_url, self.supabase_key)
    
    def is_valid_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def is_valid_password(self, password: str) -> bool:
        """Validate password strength"""
        if len(password) < 8:
            return False
        # Check for at least one uppercase, one lowercase, one digit
        if not re.search(r'[A-Z]', password):
            return False
        if not re.search(r'[a-z]', password):
            return False
        if not re.search(r'\d', password):
            return False
        return True
    
    def register_user(self, email: str, password: str) -> Dict[str, Any]:
        """Register a new user"""
        if not self.is_valid_email(email):
            return {"success": False, "message": "Invalid email format"}
        
        if not self.is_valid_password(password):
            return {"success": False, "message": "Password must be at least 8 characters long and contain uppercase, lowercase, and digit"}
        
        try:
            response = self.supabase.auth.sign_up({
                "email": email,
                "password": password
            })
            
            if response.user:
                return {"success": True, "message": "Registration successful! Please check your email for verification."}
            else:
                return {"success": False, "message": "Registration failed. Please try again."}
        
        except Exception as e:
            error_msg = str(e)
            if "already_registered" in error_msg or "already been registered" in error_msg:
                return {"success": False, "message": "Email already registered. Please use a different email or try logging in."}
            return {"success": False, "message": f"Registration failed: {error_msg}"}
    
    def login_user(self, email: str, password: str) -> Dict[str, Any]:
        """Login user"""
        if not self.is_valid_email(email):
            return {"success": False, "message": "Invalid email format"}
        
        try:
            response = self.supabase.auth.sign_in_with_password({
                "email": email,
                "password": password
            })
            
            if response.user:
                # Store user session in Streamlit session state
                st.session_state.user = response.user
                st.session_state.access_token = response.session.access_token
                st.session_state.authenticated = True
                
                return {"success": True, "message": "Login successful!"}
            else:
                return {"success": False, "message": "Login failed. Please check your credentials."}
        
        except Exception as e:
            error_msg = str(e)
            if "invalid_credentials" in error_msg or "Invalid login credentials" in error_msg:
                return {"success": False, "message": "Invalid email or password. Please try again."}
            return {"success": False, "message": f"Login failed: {error_msg}"}
    
    def logout_user(self):
        """Logout user"""
        try:
            self.supabase.auth.sign_out()
            # Clear session state
            if 'user' in st.session_state:
                del st.session_state.user
            if 'access_token' in st.session_state:
                del st.session_state.access_token
            if 'authenticated' in st.session_state:
                del st.session_state.authenticated
            st.rerun()
        except Exception as e:
            st.error(f"Logout failed: {str(e)}")
    
    def get_current_user(self) -> Optional[Dict[str, Any]]:
        """Get current user from session"""
        if 'user' in st.session_state:
            return st.session_state.user
        return None
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        return st.session_state.get('authenticated', False)
    
    def reset_password(self, email: str) -> Dict[str, Any]:
        """Send password reset email"""
        if not self.is_valid_email(email):
            return {"success": False, "message": "Invalid email format"}
        
        try:
            response = self.supabase.auth.reset_password_email(email)
            return {"success": True, "message": "Password reset email sent! Please check your inbox."}
        except Exception as e:
            return {"success": False, "message": f"Password reset failed: {str(e)}"}



def render_auth_forms():
    """Render MusicSynth authentication forms"""
    auth = SupabaseAuth()
    
    # Apply theme
    theme_manager.apply_theme()
    
    st.markdown('<div class="auth-container musicsynth-fade-in">', unsafe_allow_html=True)
    
    # Create tabs for login and register
    tab1, tab2 = st.tabs(["🎵 Sign In", "✨ Get Started"])
    
    with tab1:
        st.markdown('<div class="musicsynth-slide-in">', unsafe_allow_html=True)
        
        with st.form("login_form", clear_on_submit=False):
            st.markdown("### Welcome Back to MusicSynth")
            st.markdown("Continue your musical journey")
            
            email = st.text_input(
                "Email",
                placeholder="Enter your email address",
                key="login_email"
            )
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password",
                key="login_password"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2 = st.columns(2)
            with col1:
                login_button = st.form_submit_button(
                    "Sign In",
                    use_container_width=True,
                    type="primary"
                )
            with col2:
                st.markdown("")  # Spacer
            
            if login_button:
                if email and password:
                    with st.spinner("Signing you in..."):
                        result = auth.login_user(email, password)
                        if result["success"]:
                            st.success(result["message"])
                            st.balloons()
                            st.rerun()
                        else:
                            st.error(result["message"])
                else:
                    st.error("Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Password reset section
        st.markdown("---")
        st.markdown("### Forgot Your Password?")
        
        with st.form("reset_form", clear_on_submit=True):
            st.markdown("No worries! Enter your email and we'll send you a reset link")
            
            reset_email = st.text_input(
                "Email",
                placeholder="Enter your email address",
                key="reset_email"
            )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            reset_button = st.form_submit_button(
                "Send Reset Link",
                use_container_width=True,
                type="secondary"
            )
            
            if reset_button:
                if reset_email:
                    with st.spinner("Sending reset email..."):
                        result = auth.reset_password(reset_email)
                        if result["success"]:
                            st.success(result["message"])
                        else:
                            st.error(result["message"])
                else:
                    st.error("Please enter your email address")
    
    with tab2:
        st.markdown('<div class="musicsynth-slide-in">', unsafe_allow_html=True)
        
        with st.form("register_form", clear_on_submit=False):
            st.markdown("### Join the MusicSynth Community")
            st.markdown("Start transforming your sheet music into visual magic today!")
            
            reg_email = st.text_input(
                "Email",
                placeholder="Enter your email address",
                key="reg_email"
            )
            
            col1, col2 = st.columns(2)
            with col1:
                reg_password = st.text_input(
                    "Password",
                    type="password",
                    placeholder="Create a strong password",
                    key="reg_password"
                )
            with col2:
                reg_confirm_password = st.text_input(
                    "Confirm Password",
                    type="password",
                    placeholder="Confirm your password",
                    key="reg_confirm_password"
                )
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            register_button = st.form_submit_button(
                "Start Creating",
                use_container_width=True,
                type="primary"
            )
            
            if register_button:
                if reg_email and reg_password and reg_confirm_password:
                    if reg_password != reg_confirm_password:
                        st.error("Passwords do not match")
                    else:
                        with st.spinner("Creating your account..."):
                            result = auth.register_user(reg_email, reg_password)
                            if result["success"]:
                                st.success(result["message"])
                                st.balloons()
                            else:
                                st.error(result["message"])
                else:
                    st.error("Please fill in all fields")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Password requirements with MusicSynth styling
        st.markdown("""
        <div class="password-requirements">
            <h4>🔐 Password Requirements</h4>
            <ul>
                <li>At least 8 characters long</li>
                <li>Contains uppercase and lowercase letters</li>
                <li>Contains at least one digit</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Developer note from the website
    st.markdown("""
    <div class="developer-note">
        <h4>Built with Passion ❤️</h4>
        <p>Created by a high school student passionate about music education technology</p>
    </div>
    """, unsafe_allow_html=True)
    
    # MusicSynth footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; padding: 24px; opacity: 0.7;">
        <p style="margin: 0; font-size: 0.9rem;">
            🎼 <strong>Transform</strong> • 🎨 <strong>Visualize</strong> • 🚀 <strong>Learn</strong>
        </p>
        <p style="margin: 8px 0 0 0; font-size: 0.8rem; opacity: 0.6;">
            Built with Python, Streamlit, MuseScore, and ❤️
        </p>
    </div>
    """, unsafe_allow_html=True)


def require_auth():
    """Decorator-like function to require authentication"""
    auth = SupabaseAuth()
    
    if not auth.is_authenticated():
        # Apply theme first
        theme_manager.apply_theme()
        
        # MusicSynth authentication page
        st.markdown("""
        <div style="text-align: center; padding: 3rem 1.5rem;">
            <h1 style="font-size: 2.5rem; margin-bottom: 1rem; color: var(--foreground); font-weight: 700;">
                🎵 MusicSynth
            </h1>
            <p style="font-size: 1.125rem; margin-bottom: 0.5rem; color: var(--foreground); font-weight: 500;">
                Transform Sheet Music into Visual Magic
            </p>
            <p style="font-size: 1rem; opacity: 0.8; margin-bottom: 2rem; color: var(--muted-foreground); font-style: italic;">
                Sign in to experience the future of music learning
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        render_auth_forms()
        return False
    
    return True


def render_user_menu():
    """Render MusicSynth user menu in sidebar"""
    auth = SupabaseAuth()
    
    if auth.is_authenticated():
        user = auth.get_current_user()
        if user:
            st.sidebar.markdown("""
            <div class="sidebar-user">
                <h3 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-weight: 600;">🎵 Welcome!</h3>
                <p style="margin: 0; font-size: 0.875rem; color: var(--muted-foreground);">{}</p>
            </div>
            """.format(user.email), unsafe_allow_html=True)
            
            # Logout button
            if st.sidebar.button("🚪 Sign Out", use_container_width=True, type="secondary"):
                auth.logout_user()
        
        # Usage statistics
        st.sidebar.markdown("---")
        st.sidebar.markdown("""
        <div class="musicsynth-card">
            <h3 style="margin: 0 0 0.5rem 0; color: var(--foreground); font-size: 1rem;">🎼 Your Session</h3>
            <p style="margin: 0; font-size: 0.875rem; color: var(--muted-foreground);">Ready to create musical magic!</p>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        st.sidebar.markdown("""
        <div class="sidebar-user">
            <h3 style="margin: 0 0 0.5rem 0; color: var(--muted-foreground); font-weight: 600;">🔒 Sign In Required</h3>
            <p style="margin: 0; font-size: 0.875rem; color: var(--muted-foreground);">Please sign in to start creating</p>
        </div>
        """, unsafe_allow_html=True) 