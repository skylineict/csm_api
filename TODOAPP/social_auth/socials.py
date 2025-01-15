from fastapi_sso.sso.google import GoogleSSO
from fastapi_sso.sso.facebook import FacebookSSO
from fastapi import Request
import os



import os
from dotenv import load_dotenv
from some_oauth_library import GoogleSSO, FacebookSSO  # Replace with your actual library

load_dotenv()  # Load environment variables from .env file

google_sso = GoogleSSO(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    redirect_uri=os.getenv("GOOGLE_REDIRECT_URI"),
)

facebook_sso = FacebookSSO(
    client_id=os.getenv("FACEBOOK_CLIENT_ID"),
    client_secret=os.getenv("FACEBOOK_CLIENT_SECRET"),
    redirect_uri=os.getenv("FACEBOOK_REDIRECT_URI"),
    scope=os.getenv("FACEBOOK_SCOPE"),
)

