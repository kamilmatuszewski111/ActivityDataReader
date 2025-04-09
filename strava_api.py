import requests
import time
import json
from loguru import logger
from collections import defaultdict
import os
from dotenv import load_dotenv

TOKEN_URL = "https://www.strava.com/oauth/token"
ACTIVITIES_URL = "https://www.strava.com/api/v3/athlete/activities"
AUTHORIZATION_CODE = "d26dc961f305425071a6218b62b7e86afe33d2c7"

# response = requests.post(TOKEN_URL, data={
#     "client_id": loaded_tokens["CLIENT_ID"],
#     "client_secret": loaded_tokens["CLIENT_SECRET"],
#     "code": AUTHORIZATION_CODE,
#     "grant_type": "authorization_code"
# })


class StravaAPI:
    def __init__(self):
        self.loaded_tokens = defaultdict()
        self._load_tokens()
        load_dotenv()

    def _save_to_env(self, data: dict):
        logger.info("Saving data to .env file.")
        with open(".env", "w") as file:
            for key, value in data.items():
                file.write(f"{key.upper()}={value}\n")

    def _load_tokens(self):
        logger.info("Loading tokens from env file.")
        # with open("api_tokens.json", "r", encoding="utf-8") as file:
        #     self.loaded_tokens = json.load(file)
        self.loaded_tokens["CLIENT_ID"] = os.getenv("CLIENT_ID")
        self.loaded_tokens["CLIENT_SECRET"] = os.getenv("CLIENT_SECRET")
        self.loaded_tokens["ACCESS_TOKEN"] = os.getenv("ACCESS_TOKEN")
        self.loaded_tokens["REFRESH_TOKEN"] = os.getenv("REFRESH_TOKEN")
        self.loaded_tokens["EXPIRES_AT"] = os.getenv("EXPIRES_AT")
        return self.loaded_tokens

    @staticmethod
    def _is_token_expired(expires_at):
        return time.time() > expires_at

    def refresh_token(self):
        logger.info("Start refresh token.")
        loaded_tokens = self._load_tokens()
        response = requests.post(TOKEN_URL, data={
            "client_id": loaded_tokens["CLIENT_ID"],
            "client_secret": loaded_tokens["CLIENT_SECRET"],
            "refresh_token": loaded_tokens["REFRESH_TOKEN"],
            "grant_type": "refresh_token"
        })

        if response.status_code == 200:
            logger.success("Token refresh procedure performed successfully.")
            data = response.json()

            data["CLIENT_ID"] = self.loaded_tokens["CLIENT_ID"]
            data["CLIENT_SECRET"] = self.loaded_tokens["CLIENT_SECRET"]
            self._save_to_env(data)

        else:
            logger.error("Refreshing token procedure failed.")
            logger.info(f"Details: {response.json()}")

    def check_token_expiration(self):
        logger.info(f"Checking if token is expired")
        if self._is_token_expired(self.loaded_tokens["EXPIRES_AT"]):
            logger.warning("Token is expired. Refresh token required.")
            self.refresh_token()
            self._load_tokens()
        else:
            logger.success("Token is not expired. Send API request allowed.")

    def send_request(self):
        self.check_token_expiration()
        headers = {"Authorization": f"Bearer {self.loaded_tokens['ACCESS_TOKEN']}"}

        logger.info("Create datetime params.")

        # params = {
        #     'keys': 'heartrate,velocity_smooth',
        #     'key_by_type': 'true',
        # }
        after = int(time.mktime(time.strptime('2025-01-01', '%Y-%m-%d')))
        before = int(time.mktime(time.strptime('2025-04-07', '%Y-%m-%d')))
        params = {
            'after': after,
            'before': before,
            'per_page': 99
        }

        logger.info("Sending request...")
        response = requests.get(ACTIVITIES_URL, headers=headers, params=params)

        if response.status_code == 200:
            logger.success("Response from server received correctly.")
            activities = response.json()
            for activity in activities:
                print(f"Aktywność: {activity['name']}, Typ: {activity['type']}, Dystans: {activity['distance']} m")
        else:
            logger.error("Response from server received incorrectly.", response.status_code, response.text)
            print("Error:", response.status_code, response.text)


kupa = StravaAPI()
kupa.send_request()
