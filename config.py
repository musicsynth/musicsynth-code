"""
Configuration file for MusicSynth application

Environment Variables Required:
- SUPABASE_URL: Your Supabase project URL
- SUPABASE_ANON_KEY: Your Supabase anonymous key
- STREAMLIT_SERVER_ENVIRONMENT: Set to 'production' for production deployment

Create a .env file in your project root with these variables:
SUPABASE_URL=your_supabase_project_url
SUPABASE_ANON_KEY=your_supabase_anon_key
STREAMLIT_SERVER_ENVIRONMENT=production
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Supabase Configuration
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY")

# App Configuration
STREAMLIT_SERVER_ENVIRONMENT = os.getenv("STREAMLIT_SERVER_ENVIRONMENT", "local")
IS_PRODUCTION = STREAMLIT_SERVER_ENVIRONMENT == "production"

# Validate required environment variables
def validate_config():
    """Validate that all required environment variables are set"""
    missing_vars = []
    
    if not SUPABASE_URL:
        missing_vars.append("SUPABASE_URL")
    if not SUPABASE_ANON_KEY:
        missing_vars.append("SUPABASE_ANON_KEY")
    
    if missing_vars:
        raise ValueError(f"Missing required environment variables: {', '.join(missing_vars)}")
    
    return True 