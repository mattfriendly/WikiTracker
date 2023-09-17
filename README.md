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
tracking_base_url = "https://apis.fedex.com/track/v1/trackingnumbers"

```

*wikiship.py*

Replace these with your FedEx Ship API credentials, which are different than your FedEx Track API credentials.
It is better to have different environment variable names so that the keys won't conflict with *wikitrack.py*

The environment variables are as follows:
<br>
<br>
**FedEx API Environment Variables:**
```
CLIENT_ID_ENV_VAR = "CLIENT_ID_ENV_VAR" (your FedEx SHIP API Key)
CLIENT_SECRET_ENV_VAR = "CLIENT_SECRET_ENV_VAR" (your FedEx SHIP API Secret)
ACCOUNT_NUMBER_ENV_VAR = "FEDEX_ACCOUNT_NUMBER" (your FedEx 9-digit account number)
```

**MySQL Environment Variables:**
```
DB_HOST = database host
DB_NAME = database name
DB_PASSWORD = database pass
DB_USER = database user
```

**Local Environment Variables** (soon to be replaced):
```
SHIPPING_ID = specify table ID to print label for (env var for now)
```


*mysql-schema.sql* 

This schema contains all of the necessary fields to interact with the FedEx Ship API. 