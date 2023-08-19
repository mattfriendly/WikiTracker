import os
import requests
from openai import ChatCompletion

# Replace with your FedEx API credentials
client_id = "your_client_id_here"
client_secret = "your_client_secret_here"
token_url = "https://apis-sandbox.fedex.com/oauth/token"
tracking_base_url = "https://apis-sandbox.fedex.com/track/v1/trackingnumbers"

# Replace with your OpenAI API key
api_key = "your_openai_api_key_here"


def get_access_token():
    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=payload)

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print("Access Token obtained:", access_token)
        return access_token
    else:
        print("Token Request failed with status code:", response.status_code)
        return None


def get_tracking_info(tracking_number, access_token):
    if not access_token:
        print("Access token is not available.")
        return

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    payload = {
        # Fill in the JSON payload as required by FedEx's API
        "key": "value"
    }

    # Send a POST request with JSON payload
    response = requests.post(f"{tracking_base_url}/{tracking_number}", headers=headers, json=payload)

    if response.status_code == 200:
        data = response.json()
        print("Tracking Information:", data)
    else:
        print("API Request failed with status code:", response.status_code)


def main():
    tracking_number = "your_tracking_number_here"

    access_token = get_access_token()  # Obtain access token
    get_tracking_info(tracking_number, access_token)  # Get tracking information


if __name__ == "__main__":
    main()
