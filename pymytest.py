import pymysql
import os
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

def test_mysql_ssl_connection(host, user, password, db, ssl_dict):
    try:
        # Establishing a connection using SSL
        connection = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            ssl=ssl_dict
        )

        print("Successfully connected to MySQL server using SSL!")

        # Close the connection
        connection.close()
    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL server: {e}")


if __name__ == "__main__":
    # Database configuration
    host = os.environ.get("DB_HOST")
    user = os.environ.get("DB_USER")
    password = os.environ.get("DB_PASSWORD")
    db = os.environ.get("DB_NAME")

    # SSL configuration - use environment variables for file paths
    ssl_dict = {
        'ca': os.environ.get("MYSQL_CA_CERT_PATH"),
        'verify_cert': 'false',  # You can set this as an environment variable if needed
        'key': os.environ.get("MYSQL_CLIENT_KEY_PATH"),
        'cert': os.environ.get("MYSQL_CLIENT_CERT_PATH"),
        'check_hostname': False
    }

    test_mysql_ssl_connection(host, user, password, db, ssl_dict)
