# WikiTracker

WikiTracker is a python script that will perform an OAuth 2.0 call to the FedEx production API. 
This script assumes you have a Developer account with FedEx at https://developer.fedex.com/ and will need an API key configured within the portal.

# Usage

*wikitrack.py*

Replace with your FedEx API credentials. Please note the _client_id_ and _client_secret_ are environment variables within your OS and should not be hard-coded within the script.

In your environment/OS set the two environment variables: 

**FEDEX_CLIENT_ID** is your FedEx API key (as _client_id_)

**FEDEX_CLIENT_SECRET** is your FedEx API secret (as _client_secret_)

```
CLIENT_ID_ENV_VAR = "FEDEX_CLIENT_ID"
CLIENT_SECRET_ENV_VAR = "FEDEX_CLIENT_SECRET"

token_url = "https://apis.fedex.com/oauth/token"
tracking_base_url = "https://apis.fedex.com/track/v1/trackingnumbers"```
