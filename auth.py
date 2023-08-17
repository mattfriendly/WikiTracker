import requests
import dns.resolver

# Replace with your FedEx API credentials
api_key = "your_api_key_here"
account_number = "your_account_number_here"

# Base URL for FedEx Tracking API
base_url = "https://api.e-commerce.fedex.com/v1/tracking"

def resolve_domain(domain):
    resolver = dns.resolver.Resolver()
    try:
        resolved_ips = resolver.resolve(domain)
        return resolved_ips[0].address
    except (dns.resolver.NXDOMAIN, dns.resolver.NoAnswer, dns.exception.DNSException):
        return None

def get_tracking_info(tracking_number, custom_headers=None, request_data=None):
    resolved_ip = resolve_domain("apis-sandbox.fedex.com")

    if not resolved_ip:
        print("Failed to resolve domain name.")
        return

    # Prepare the default headers with required authentication
    headers = {
        "Authorization": f"Bearer {api_key}",
        "account-number": account_number
    }

    # If custom headers are provided, update the default headers
    if custom_headers:
        headers.update(custom_headers)

    try:
        # Make a POST request to the resolved IP address using HTTPS
        url = f"https://{resolved_ip}/v1/tracking"
        response = requests.post(url, headers=headers, json=request_data)

        if response.status_code == 200:
            data = response.json()
            print("Tracking Information:", data)
        else:
            print("API Request failed with status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)

if __name__ == "__main__":
    tracking_number = "your_tracking_number_here"

    # Example: Customize headers and request body data
    custom_headers = {"custom-header": "value"}
    request_data = {"request_key": "request_value"}

    get_tracking_info(tracking_number, custom_headers, request_data)
