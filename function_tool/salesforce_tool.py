import os
import requests
from typing import Any, Dict
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def get_salesforce_credentials() -> Dict[str, str]:
    """
    Get and validate Salesforce credentials from environment variables.

    Returns:
        Dictionary containing client_id, client_secret, and token_url

    Raises:
        ValueError: If required credentials are missing
    """
    # Get credentials from environment variables
    client_id = os.getenv("SALESFORCE_CLIENT_ID")
    client_secret = os.getenv("SALESFORCE_CLIENT_SECRET")

    # Get My Domain URL and construct token URL
    my_domain_url = os.getenv("SALESFORCE_MY_DOMAIN_URL")
    # Construct token URL by appending OAuth endpoint path
    token_url = f"{my_domain_url}/services/oauth2/token"

    if not client_id or not client_secret or not my_domain_url:
        missing_vars = []
        if not client_id:
            missing_vars.append("SALESFORCE_CLIENT_ID")
        if not client_secret:
            missing_vars.append("SALESFORCE_CLIENT_SECRET")
        if not my_domain_url:
            missing_vars.append("SALESFORCE_MY_DOMAIN_URL")

        raise ValueError(
            f"Missing Salesforce credentials. Please set {', '.join(missing_vars)} "
            "in your environment variables or .env file."
        )

    return {
        "client_id": client_id,
        "client_secret": client_secret,
        "token_url": token_url,
    }


def get_salesforce_access_token() -> Dict[str, str]:
    """
    Get Salesforce access token using OAuth 2.0 Client Credentials Flow.

    Returns:
        Dictionary containing access_token and instance_url
    """
    # Get and validate credentials
    credentials = get_salesforce_credentials()
    client_id = credentials["client_id"]
    client_secret = credentials["client_secret"]
    token_url = credentials["token_url"]

    # Prepare token request
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
    }

    # Request access token
    response = requests.post(token_url, data=data)
    response.raise_for_status()

    token_data = response.json()
    return {
        "access_token": token_data.get("access_token"),
        "instance_url": token_data.get("instance_url"),
    }


def salesforce_soql_tool(soql_query: str) -> Any:
    """
    Execute a SOQL query against Salesforce using OAuth 2.0 Client Credentials Flow.

    Args:
        soql_query: A SOQL query string (e.g., "SELECT Id, Name FROM Account LIMIT 10")

    Returns:
        Query results as a dictionary containing the records and metadata

    Raises:
        ValueError: If credentials are missing or invalid
        requests.exceptions.RequestException: If the API request fails

    Example:
        >>> result = salesforce_soql_tool("SELECT Id, Name FROM Account LIMIT 5")
        >>> print(result['totalSize'])
        >>> for record in result['records']:
        ...     print(record['Name'])
    """
    try:
        # Get authentication token
        auth_data = get_salesforce_access_token()
        access_token = auth_data["access_token"]
        instance_url = auth_data["instance_url"]

        # Prepare SOQL query API endpoint
        api_version = os.getenv("SALESFORCE_API_VERSION", "v59.0")
        query_url = f"{instance_url}/services/data/{api_version}/query"

        # Set up headers with access token
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json",
        }

        # Execute SOQL query
        params = {"q": soql_query}
        response = requests.get(query_url, headers=headers, params=params)
        response.raise_for_status()

        # Return query results
        result = response.json()
        return result

    except requests.exceptions.RequestException as e:
        error_msg = f"Failed to execute SOQL query: {str(e)}"
        if hasattr(e.response, 'text'):
            error_msg += f"\nResponse: {e.response.text}"
        raise Exception(error_msg)
    except Exception as e:
        raise Exception(f"Error executing SOQL query: {str(e)}")

