
import time
import json
import requests
from django.conf import settings as app_settings

URL = app_settings.SSO_URL

# settings.configure()
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SSO.settings")


class SSO:
    """_summary_
    SSO CLASS
    """

    def __init__(self, sp_api_key, sp_hash_key, session_key) -> None:
        self.api = sp_api_key
        self.hash = sp_hash_key
        self.check_credentials(sp_api_key, sp_hash_key, session_key)

    @staticmethod
    def check_credentials(api_key: str, hash_key: str, session_key: str):
        """_summary_
            checks the session and returns session status
        """
        try:
            headers = {
                "api-key": api_key,
                "hash-key":  hash_key,
                "request-ts": int(time.time())
            }
            response = requests.get(f"{URL}/{session_key}", headers=headers)
            data = json.loads(response.text)
            return data

        except Exception as e:
            return f"Something went wrong, please confirm the credentials and try again: {e}"
