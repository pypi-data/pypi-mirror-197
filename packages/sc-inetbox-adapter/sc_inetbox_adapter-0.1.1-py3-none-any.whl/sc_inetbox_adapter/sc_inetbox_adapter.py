import json
import requests
import urllib3
import http


class InternetboxAdapter:

    def __init__(self, admin_password: str, protocol: str = "https", ip_address: str = "192.168.1.1") -> None:
        self._admin_password = admin_password
        self._protocol = protocol
        self._ip_address = ip_address
        self._auth_token = None
        self._session = requests.Session()

    def create_session(self) -> http.HTTPStatus:
        payload = json.dumps({"service": "sah.Device.Information", "method": "createContext", "parameters": {
                             "applicationName": "webui", "username": "admin", "password": self._admin_password}})
        headers = {
            'Authorization': 'X-Sah-Login'
        }
        response = self._send_ws_request(payload, headers)
        if response.status_code == http.HTTPStatus.OK:
            self._auth_token = response.json()['data']['contextID']
        return response.status_code

    def logout_session(self) -> http.HTTPStatus:

        payload = json.dumps({"service": "sah.Device.Information",
                             "method": "releaseContext", "parameters": {"applicationName": "webui"}})
        headers = {
            'Authorization': 'X-Sah-Logout %s' % (self._auth_token)
        }
        response = self._send_auth_ws_request(payload, headers)
        return response.status_code

    def get_software_version(self) -> str:
        payload = json.dumps(
            {"service": "APController", "method": "getSoftWareVersion", "parameters": {}})
        response = self._send_ws_request(payload)
        if response.status_code == http.HTTPStatus.OK:
            return response.json()["data"]["version"]
        else:
            return "HTTP status code %d, check authentication" % (response.status_code)

    def get_devices(self) -> json:

        payload = json.dumps({
            "service": "Devices",
            "method": "get",
            "parameters": {
                "expression": "lan and not self",
                "flags": "no_actions"
            }
        })

        response = self._send_auth_ws_request(payload)
        if response.status_code == http.HTTPStatus.OK:
            return response.json()["status"]
        else:
            return {"error": "Got HTTP status code %d, check authentication" % (response.status_code)}

    def _send_ws_request(self, payload: str, headers={}) -> requests.Response:
        url = "%s://%s/ws" % (self._protocol, self._ip_address)
        headers['Content-Type'] = 'application/x-sah-ws-4-call+json'
        # TODO find solution with certcheck
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
        # TODO exception handling
        response = self._session.post(
            url, headers=headers, data=payload, verify=False)
        # print(json.dumps(response.json(), indent=2))
        return response

    def _send_auth_ws_request(self, payload: str, headers={}) -> requests.Response:
        if not self._auth_token:
            raise Exception(
                "No active session, create one first by calling create_session")
        headers['X-Context'] = self._auth_token
        return self._send_ws_request(payload, headers)
