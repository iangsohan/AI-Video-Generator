import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

def get_authenticated_service():
    """
    This function obtains an authenticated service object for accessing the YouTube API.
    It checks if credentials are available and valid. If not, it initiates an OAuth 2.0
    authentication flow to obtain or refresh credentials. Finally, it returns a service
    object initialized with the obtained credentials.
    """
    credentials = None

    # Check if the credentials file exists
    if os.path.exists('auth/credentials.pickle'):
        with open('auth/credentials.pickle', 'rb') as token:
            credentials = pickle.load(token)

    # If credentials are invalid or not available, authenticate the user
    if not credentials or not credentials.valid:
        # Check if credentials are expired and refresh token is available
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            # Create OAuth 2.0 flow using client_secrets.json file
            flow = InstalledAppFlow.from_client_secrets_file(
                "auth/client_secrets.json",
                scopes=[
                    "https://www.googleapis.com/auth/youtube.force-ssl",
                    "https://www.googleapis.com/auth/youtube.upload"
                ]
            )
            credentials = flow.run_local_server()
        # Save the updated credentials to the pickle file
        with open('auth/credentials.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    # Return a YouTube service object initialized with the obtained credentials
    return build('youtube', 'v3', credentials=credentials)