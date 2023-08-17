import requests
from requests_oauthlib import OAuth2Session

# Replace with your OAuth 2.0 credentials
client_id = "l766ea65f0fc674f669c6ba15463093de0"
client_secret = "3abe48b5a51145afbdcb0d2924738cb6"
authorization_base_url = "https://apis-sandbox.fedex.com/oauth/token"
token_url = "https://apis-sandbox.fedex.com/oauth/token"
redirect_uri = "https://your-redirect-uri.com/callback"


def authenticate_with_oauth():
    oauth = OAuth2Session(client_id, redirect_uri=redirect_uri)
    authorization_url, _ = oauth.authorization_url(authorization_base_url)

    print("Please go to the following URL and authorize the application:")
    print(authorization_url)

    authorization_response = input("Enter the full callback URL after authorization: ")
    token = oauth.fetch_token(token_url, authorization_response=authorization_response, client_secret=client_secret)

    api_url = "https://api.example.com/resource"  # Replace with your API URL

    try:
        response = oauth.get(api_url)

        if response.status_code == 200:
            data = response.json()
            # Process the API response data
            print("API Response:", data)
        else:
            print("API Request failed with status code:", response.status_code)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    authenticate_with_oauth()