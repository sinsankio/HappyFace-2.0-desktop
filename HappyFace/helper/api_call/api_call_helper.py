import requests


class ApiCallHelper:
    def put(self, url_endpoint: str, data: dict) -> dict:
        response = requests.put(url_endpoint, json=data)

        if response.status_code == 200:
            return response.json()

    def post(self, url_endpoint: str, data: dict) -> dict:
        response = requests.post(url_endpoint, json=data)

        if response.status_code == 200:
            return response.json()
