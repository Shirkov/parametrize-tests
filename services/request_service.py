import requests
import logging

LOG = logging.getLogger("log")


class Request:
    def __init__(self, url):
        self.session = requests.session()
        self.url = url

    def rpc_request(self, params):
        try:
            result = self.session.post(url=self.url,
                                       json=params)
            response = result.json()
            print(response)
            error = response.get("error")
            if error:
                LOG.error(f"Request error: {error}, {self.url}, {params}")
                LOG.exception(error)
                return None

        except requests.exceptions.RequestException as error:
            LOG.error(f"Request error: {self.url}, {params}")
            LOG.exception(error)
            return None

        except Exception as error:
            LOG.error(f"Request error: {self.url}, {params}")
            LOG.exception(error)
            return None

        return response

    def auth(self, username, password):
        return self.session.post(
            url=self.url,
            json={
                "method": "auth.login",
                "params": {
                    "username": username,
                    "password": password
                }
            })
