import json
import os
import requests
import sys

# Replace with your FedEx API credentials

CLIENT_ID_ENV_VAR = "CLIENT_ID_ENV_VAR"
CLIENT_SECRET_ENV_VAR = "CLIENT_SECRET_ENV_VAR"
ACCOUNT_NUMBER_ENV_VAR = "FEDEX_ACCOUNT_NUMBER"  # New environment variable for the account number

SHIP_BASE_URL = "https://apis-sandbox.fedex.com/ship/v1/shipments"

def get_access_token():
    # Obtain access token using OAuth2 client credentials flow
    token_url = "https://apis-sandbox.fedex.com/oauth/token"

    client_id = os.environ.get(CLIENT_ID_ENV_VAR)
    client_secret = os.environ.get(CLIENT_SECRET_ENV_VAR)

    # Print the client ID and client secret
    print(f"Client ID: {client_id}")
    print(f"Client Secret: {client_secret}")

    payload = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret
    }

    response = requests.post(token_url, data=payload)

    print("Authorization Response Status Code:", response.status_code)  # Print status code
    print("Authorization Response Content:", response.content)  # Print the entire response content

    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print("Access Token obtained:", access_token)
        return access_token
    else:
        print("Token Request failed with status code:", response.status_code)
        return None

def create_shipment_request(access_token):
    # Define the URL for the FedEx Shipments API
    url = "https://apis-sandbox.fedex.com/ship/v1/shipments"

    # Define the shipment data as a Python dictionary
    shipment_data = {
        "labelResponseOptions": "URL_ONLY",
        "requestedShipment": {
            "shipper": {
                "contact": {
                    "personName": "Jane Ng",
                    "phoneNumber": "8088561281",
                    "companyName": "KELLER WILLIAMS REALTY MAUI"
                },
                "address": {
                    "streetLines": ["212 Molehulehu St"],
                    "city": "Kahului",
                    "stateOrProvinceCode": "HI",
                    "postalCode": "96732",
                    "countryCode": "US"
                }
            },
            "recipients": [
                {
                    "contact": {
                        "personName": "Suya Chuang",
                        "phoneNumber": "4254588522",
                        "companyName": ""
                    },
                    "address": {
                        "streetLines": ["UNIT 113", "10042 MAIN STREET"],
                        "city": "BELLEVUE",
                        "stateOrProvinceCode": "WA",
                        "postalCode": "98004",
                        "countryCode": "US"
                    }
                }
            ],
            "shipDatestamp": "2023-09-19",
            "serviceType": "STANDARD_OVERNIGHT",
            "packagingType": "FEDEX_PAK",
            "pickupType": "USE_SCHEDULED_PICKUP",
            "blockInsightVisibility": False,
            "shippingChargesPayment": {
                "paymentType": "SENDER"
            },
            "labelSpecification": {
                "imageType": "PDF",
                "labelStockType": "PAPER_85X11_TOP_HALF_LABEL"
            },
            "requestedPackageLineItems": [
                {
                    "weight": {
                        "value": 10,
                        "units": "LB"
                    }
                }
            ]
        },
        "accountNumber": {
            "value": os.environ.get("FEDEX_ACCOUNT_NUMBER")  # Retrieve the account number from the environment variable
        }
    }

    # Convert the shipment data dictionary to a JSON string
    payload = json.dumps(shipment_data)

    # Define the headers with the access token
    headers = {
        'Content-Type': "application/json",
        'X-locale': "en_US",
        'Authorization': f"Bearer {access_token}"
    }

    # Make a POST request to create the shipment and obtain the shipping label
    response = requests.post(url, data=payload, headers=headers)

    print("API Response Status Code:", response.status_code)
    print("API Response Content:", response.content)

    if response.status_code == 200:
        data = response.json()
        label_url = data.get("output", {}).get("transactionShipments", [{}])[0].get("pieceResponses", [{}])[0].get(
            "packageDocuments", [{}])[0].get("url")
        return label_url  # Return the label URL
    else:
        print("Shipment creation failed with status code:", response.status_code)
        return None

def main():
    # Retrieve API credentials from environment variables
    client_id = os.environ.get(CLIENT_ID_ENV_VAR)
    client_secret = os.environ.get(CLIENT_SECRET_ENV_VAR)
    account_number = os.environ.get(ACCOUNT_NUMBER_ENV_VAR)  # Get the account number from the environment

    # Check for missing environment variables
    missing_vars = []
    if not client_id:
        missing_vars.append(CLIENT_ID_ENV_VAR)
    if not client_secret:
        missing_vars.append(CLIENT_SECRET_ENV_VAR)
    if not account_number:
        missing_vars.append(ACCOUNT_NUMBER_ENV_VAR)

    if missing_vars:
        print("Error: The following required environment variables are missing:")
        for var in missing_vars:
            print(f"- {var}")
        return

    access_token = get_access_token()  # Obtain access token

    if not access_token:
        print("Access token could not be obtained. Exiting.")
        sys.exit(1)

    # Call create_shipment_request() with the access_token
    shipment_label_url = create_shipment_request(access_token)

    if shipment_label_url:
        # Display the URL if it's available
        print("Shipping Label URL:", shipment_label_url)
    else:
        print("Shipment creation failed.")

if __name__ == "__main__":
    main()