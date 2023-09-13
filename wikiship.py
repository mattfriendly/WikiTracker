import os
import requests

# FedEx Track API Credentials

CLIENT_ID_ENV_VAR = "FEDEX_CLIENT_ID"
CLIENT_SECRET_ENV_VAR = "FEDEX_CLIENT_SECRET"
SHIP_BASE_URL = "https://apis.fedex.com/ship/v1"

def get_access_token():
    # Obtain access token using OAuth2 client credentials flow
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
def create_shipment(access_token, shipment_data):
    # Create a shipment using the FedEx Ship API
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
    # Retrieve API credentials from environment variables
    client_id = os.environ.get(CLIENT_ID_ENV_VAR)
    client_secret = os.environ.get(CLIENT_SECRET_ENV_VAR)

    access_token = get_access_token()  # Obtain access token

    # Customize your shipment data (e.g., recipient details, package information, etc.)
    shipment_data = {
        # Add your shipment data here
    }

    # Create a shipment and obtain the shipping label
    shipment_label = create_shipment(access_token, shipment_data)

    if shipment_label:
        # Save or process the shipping label as needed
        # ... (e.g., save it as a PDF or print it)
    else:
        print("Shipment creation failed.")

if __name__ == "__main__":
    main()
