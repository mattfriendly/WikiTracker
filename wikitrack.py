import os
import requests


# Replace with your FedEx API credentials

WEBHOOK_URL = "WEBHOOK_URL"
CLIENT_ID_ENV_VAR = "FEDEX_CLIENT_ID"
CLIENT_SECRET_ENV_VAR = "FEDEX_CLIENT_SECRET"

token_url = "https://apis.fedex.com/oauth/token"
tracking_base_url = "https://apis.fedex.com/track/v1/trackingnumbers"

# Set the environment variable

# os.environ["WEBHOOK_URL"] = ""

def get_access_token():
    client_id = os.environ.get(CLIENT_ID_ENV_VAR)
    client_secret = os.environ.get(CLIENT_SECRET_ENV_VAR)

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=payload)

    print("Authorization Response Content:", response.content)  # Print the entire response content / debug

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
        "includeDetailedScans": 'True',
        "trackingInfo": [
            {
                "shipDateBegin": "",
                "shipDateEnd": "",
                "trackingNumberInfo": {
                    "trackingNumber": f"{tracking_number}",
                    "carrierCode": "FDXE",
                    "trackingNumberUniqueId": ""
                }
            }
        ]
    }

    # Send a POST request with JSON payload
    response = requests.post(tracking_base_url, headers=headers, json=payload)

    print("API Response Status Code:", response.status_code)
    print("API Response Content:", response.content)

    if response.status_code == 200:
        data = response.json()
        print("Tracking Information:", data)
    else:
        print("API Request failed with status code:", response.status_code)


def main():
    # Fetch data from the webhook
    webhook_data = fetch_data_from_webhook()

    # Process the webhook data using the handler
    if webhook_data:
        webhook_handler(webhook_data)
    else:
        print("No webhook data found.")
        # Prompt the user for input as a fallback
        user_input = input("Please enter a tracking number: ")
        if user_input:
            access_token = get_access_token()  # Obtain access token
            get_tracking_info(user_input, access_token)  # Get tracking information
        else:
            print("No user input provided. Exiting.")

if __name__ == "__main__":
    main()