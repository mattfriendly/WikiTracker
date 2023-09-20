#WikiShip.py
#Coded with friendliness

import json
import os
import requests
import sys
import mysql.connector
import pymysql
from datetime import datetime

# Print the current working directory
print("Current Working Directory:", os.getcwd())

# Replace with your FedEx API credentials & and variables from the environment

# DB_USER = database username
# DB_PASS = database password
# DB_HOST = database hostname
# DB_NAME = database name

# SHIPMENT_ID = meant to be pulled in dynamically but for now define it statically in the env

CLIENT_ID_ENV_VAR = "TEST_CLIENT_ID_ENV_VAR"
CLIENT_SECRET_ENV_VAR = "TEST_CLIENT_SECRET_ENV_VAR"
ACCOUNT_NUMBER_ENV_VAR = "FEDEX_ACCOUNT_NUMBER"
SHIPMENT_ID_ENV_VAR = "SHIPMENT_ID"
TABLE_NAME_ENV_VAR = "HFC_SHIPMENTS_TABLE"

SHIP_BASE_URL = "https://apis-sandbox.fedex.com/ship/v1/shipments"

# Define a custom JSON encoder for datetime objects
class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            # Convert datetime object to a string in ISO 8601 format
            return obj.isoformat()
        return super().default(obj)
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

import pymysql

def get_shipment_data_from_mysql(shipment_id):
    # Retrieve database configuration from environment variables
    db_host = os.environ.get("DB_HOST")
    db_user = os.environ.get("DB_USER")
    db_password = os.environ.get("DB_PASSWORD")
    db_name = os.environ.get("DB_NAME")

    # Ensure that all required environment variables are set
    if None in [db_host, db_user, db_password, db_name]:
        print("Error: Missing one or more database configuration environment variables.")
        return None

    # Connect to the MySQL database using the retrieved environment variables
    db_config = {
        "host": db_host,
        "user": db_user,
        "password": db_password,
        "database": db_name,
        "ssl_ca": "ca.pem",  # Replace with the path to your CA certificate file
        "ssl_cert": "client-cert.pem",  # Replace with the path to your client certificate file
        "ssl_key": "client-key.pem",  # Replace with the path to your client key file
    }

    # Establish a connection using pymysql
    connection = pymysql.connect(**db_config)
    cursor = connection.cursor(pymysql.cursors.DictCursor)  # Use a dictionary cursor

    try:
        # Retrieve the table name from the environment variable
        table_name = os.environ.get(TABLE_NAME_ENV_VAR)  # Use a default value if not set

        # Create the SQL query using the table name
        query = f"SELECT * FROM {table_name} WHERE order_id = %s"
        cursor.execute(query, (shipment_id,))
        shipment_data = cursor.fetchone()
    except pymysql.Error as e:
        print("MySQL Error:", e)
        shipment_data = None  # Set shipment_data to None in case of an error

    print("Retrieved Shipment Data:", shipment_data)  # Add this line for debugging

    cursor.close()
    connection.close()

    # Check if shipment_data is not None
    if shipment_data:
        # Access the ship_datestamp value by its column name
        ship_datestamp = shipment_data.get('ship_datestamp')

        # Convert the 'ship_datestamp' field to a Python datetime object
        if ship_datestamp:
            try:
                ship_datestamp = datetime.strptime(str(ship_datestamp), '%Y-%m-%d %H:%M:%S')
            except ValueError as e:
                print("Warning: Unable to convert 'ship_datestamp' to Python datetime:", e)
        else:
            print("Warning: 'ship_datestamp' is None in the database.")

        # Now you have the ship_datestamp as a datetime object
        # You can return it or process it further as needed

    # Add this print statement to verify the returned data
    print("Returning Shipment Data:", shipment_data)
    return shipment_data  # Return the shipment data

def create_shipment_request(access_token, shipment_data):
    # Define the URL for the FedEx Shipments API
    url = "https://apis-sandbox.fedex.com/ship/v1/shipments"

    # Continue defining the rest of the shipment data fields using the retrieved data
    shipment_data_dict = {
        "labelResponseOptions": "URL_ONLY",
        "requestedShipment": {
            "shipper": {
                "contact": {
                    "personName": shipment_data["shipper_name"],
                    "phoneNumber": shipment_data["shipper_phone"],
                    "companyName": shipment_data["shipper_company"],
                },
                "address": {
                    "streetLines": [shipment_data["shipper_street"]],
                    "city": shipment_data["shipper_city"],
                    "stateOrProvinceCode": shipment_data["shipper_state"],
                    "postalCode": shipment_data["shipper_postal"],
                    "countryCode": shipment_data["shipper_country"],
                }
            },
            "recipients": [
                {
                    "contact": {
                        "personName": shipment_data["recipient_name"],
                        "phoneNumber": shipment_data["recipient_phone"],
                        "companyName": shipment_data["recipient_company"],
                    },
                    "address": {
                        "streetLines": [shipment_data["recipient_street1"], shipment_data["recipient_street2"]],
                        "city": shipment_data["recipient_city"],
                        "stateOrProvinceCode": shipment_data["recipient_state"],
                        "postalCode": shipment_data["recipient_postal"],
                        "countryCode": shipment_data["recipient_country"],
                    }
                }
            ],
            "shipDatestamp": shipment_data["ship_datestamp"],
            "serviceType": shipment_data["service_type"],
            "packagingType": shipment_data["packaging_type"],
            "pickupType": shipment_data["pickup_type"],
            "blockInsightVisibility": shipment_data["block_insight_visibility"],
            "shippingChargesPayment": {
                "paymentType": "SENDER",
                "payor": {
                    "responsibleParty": {
                        "address": {
                            "streetLines": [
                                shipment_data["shipping_charges_street1"],
                                shipment_data["shipping_charges_street2"]
                            ],
                            "city": shipment_data["shipping_charges_city"],
                            "stateOrProvinceCode": shipment_data["shipping_charges_state"],
                            "postalCode": shipment_data["shipping_charges_postal"],
                            "countryCode": shipment_data["shipping_charges_country"],
                            "residential": shipment_data["shipping_charges_residential"]
                        },
                        "contact": {
                            "personName": shipment_data["shipping_charges_person_name"],
                            "emailAddress": shipment_data["shipping_charges_email"],
                            "phoneNumber": shipment_data["shipping_charges_phone"],
                            "phoneExtension": shipment_data["shipping_charges_phone_extension"],
                            "companyName": shipment_data["shipping_charges_company_name"],
                            "faxNumber": shipment_data["shipping_charges_fax_number"]
                        },
                        "accountNumber": {
                            "value": os.environ.get(ACCOUNT_NUMBER_ENV_VAR)
                        }
                    }
                }
            },
            "labelSpecification": {
                "imageType": shipment_data["image_type"],
                "labelStockType": shipment_data["label_stock_type"],
            },
            "requestedPackageLineItems": [
                {
                    "weight": {
                        "value": shipment_data["weight_value"],
                        "units": "LB"
                    }
                }
            ]
        },
        "accountNumber": {
            "value": os.environ.get(ACCOUNT_NUMBER_ENV_VAR)
        }
    }

    # Debug: Print each value in the shipment_data_dict
    for key, value in shipment_data_dict.items():
        print(f"{key}: {value}")

    # Convert the shipment data dictionary to a JSON string
    payload = json.dumps(shipment_data_dict, cls=DateTimeEncoder)

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

    # Retrieve shipment ID from the environment variable
    shipment_id = os.environ.get(SHIPMENT_ID_ENV_VAR)

    # Retrieve table name from the environment variable
    table_name = os.environ.get(TABLE_NAME_ENV_VAR)  # Use a default value if not set

    # Check for missing environment variables
    missing_vars = []
    if not client_id:
        missing_vars.append(CLIENT_ID_ENV_VAR)
    if not client_secret:
        missing_vars.append(CLIENT_SECRET_ENV_VAR)
    if not account_number:
        missing_vars.append(ACCOUNT_NUMBER_ENV_VAR)
    if not shipment_id:
        missing_vars.append(SHIPMENT_ID_ENV_VAR)
    if not table_name:
        missing_vars.append(TABLE_NAME_ENV_VAR)


    if missing_vars:
        print("Error: The following required environment variables are missing:")
        for var in missing_vars:
            print(f"- {var}")
        return

    access_token = get_access_token()  # Obtain access token

    if not access_token:
        print("Access token could not be obtained. Exiting.")
        sys.exit(1)

    # Ensure that the shipment ID is an integer
    try:
        shipment_id = int(shipment_id)
    except ValueError:
        print("Error: Invalid shipment ID. It must be an integer.")
        sys.exit(1)

    shipment_data = get_shipment_data_from_mysql(shipment_id)

    print("Shipment ID:", shipment_id)
    print("Retrieved Shipment Data:", shipment_data)

    if shipment_data:
        # Call create_shipment_request() with the access_token and shipment_data
        shipment_label_url = create_shipment_request(access_token, shipment_data)

        if shipment_label_url:
            # Display the URL if it's available
            print("Shipping Label URL:", shipment_label_url)
        else:
            print("Shipment creation failed.")
    else:
        print("Shipment data not found in the database.")


if __name__ == "__main__":
    main()