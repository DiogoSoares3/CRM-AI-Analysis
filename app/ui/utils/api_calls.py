import requests

def api_request(api_url: str, json=None):
    """
    Sends an HTTP GET or POST request to the specified API URL.

    Args:
        api_url (str): 
            The URL of the API endpoint.
        json (dict | None, optional): 
            The JSON payload for a POST request (None for GET requests).

    Returns:
        response (list | dict): 
            The JSON response from the API, or an empty list if an error occurs.
    """
    try:
        if json:
            response = requests.post(api_url, json=json)
        else:
            response = requests.get(api_url)
            
        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error occurred: {err}")
        return []
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
        return []
