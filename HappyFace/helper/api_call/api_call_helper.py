import requests


class ApiCallHelper:
    @staticmethod
    def put(url_endpoint: str, data: dict) -> dict:
        response = requests.put(url_endpoint, json=data)

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def post(url_endpoint: str, data: dict | None = None) -> dict:
        response = requests.post(url_endpoint, json=data)

        if response.status_code == 200:
            return response.json()
