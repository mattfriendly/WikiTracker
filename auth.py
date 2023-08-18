import os
import requests
from requests_oauthlib import OAuth2Session

# Replace with your FedEx API credentials
client_id = "your_client_id_here"
client_secret = "your_client_secret_here"
token_url = "https://apis-sandbox.fedex.com/v1/oauth/token"
authorization_base_url = "https://apis-sandbox.fedex.com/v1/oauth/authorize"
tracking_base_url = "https://apis.fedex.com/v1/tracking"


def authenticate():
    oauth2_session = OAuth2Session(client_id, redirect_uri="http://localhost")
    authorization_url, _ = oauth2_session.authorization_url(authorization_base_url)

    print("Please go to this URL and grant access:", authorization_url)
    authorization_code = input("Enter the authorization code from the callback URL: ")

    token = oauth2_session.fetch_token(
        token_url,
        authorization_response=authorization_code,
        client_secret=client_secret
    )

    os.environ["FEDEX_ACCESS_TOKEN"] = token["access_token"]
    print("Access token stored as environment variable.")


def get_tracking_info(tracking_number):
    access_token = os.environ.get("FEDEX_ACCESS_TOKEN")
    if not access_token:
        print("Access token is not available. Please authenticate.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "account-number": "your_account_number_here"
    }

    response = requests.get(f"{tracking_base_url}/{tracking_number}", headers=headers)

    if response.status_code == 200:
        data = response.json()
        print("Tracking Information:", data)
    else:
        print("API Request failed with status code:", response.status_code)


if __name__ == "__main__":
    tracking_number = "your_tracking_number_here"

    authenticate()  # Perform OAuth 2.0 authentication
    get_tracking_info(tracking_number)  # Get tracking information
