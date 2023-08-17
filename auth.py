import requests

# Replace with your FedEx API credentials
api_key = "your_api_key_here"
account_number = "your_account_number_here"

# Base URL for FedEx Tracking API
base_url = "https://api.e-commerce.fedex.com/v1/tracking"

def get_tracking_info(tracking_number, custom_headers=None, query_params=None, request_data=None):
    # Prepare the default headers with required authentication
    headers = {
        "Authorization": f"Bearer {api_key}",
        "account-number": account_number
    }

    # If custom headers are provided, update the default headers
    if custom_headers:
        headers.update(custom_headers)

    # Prepare the default query parameters with tracking number
    params = {
        "tracking_number": tracking_number
    }

    # If additional query parameters are provided, update the defaults
    if query_params:
        params.update(query_params)

    try:
        # Make a GET request to the FedEx Tracking API
        response = requests.get(base_url, headers=headers, params=params, json=request_data)

        # Check the response status code
        if response.status_code == 200:
            data = response.json()
            # Process the tracking information
            print("Tracking Information:", data)
        else:
            print("API Request failed with status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    tracking_number = "your_tracking_number_here"

    # Example: Customize headers, query parameters, and request body data
    custom_headers = {"custom-header": "value"}
    query_params = {"additional_param": "value"}
    request_data = {"request_key": "request_value"}

    # Call the function with provided parameters
    get_tracking_info(tracking_number, custom_headers, query_params, request_data)
