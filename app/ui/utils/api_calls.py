import requests


def api_request(api_url: str, json=None):
    try:
        if json:
            response = requests.post(api_url, json=json)
        else:
            response = requests.get(api_url)

        response.raise_for_status()
        return response.json()

    except requests.exceptions.HTTPError as err:
        print(f"HTTP Error occurred: {err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")

    return []
