import requests
import pytest
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@pytest.fixture()
def get_auth_token():
    auth = {"UserName": "root", "Password": "0penBmc"}
    url = "https://localhost:2443/redfish/v1/SessionService/Sessions"
    response = requests.post(url, json=auth, headers={"Content-Type": "application/json"},verify=False)
    return response

def test_auth_openbmc(get_auth_token):
    try:
        assert "X-Auth-Token" in get_auth_token.headers
        assert get_auth_token.status_code == 201
    except Exception:
        print('Какая то из проверок не прошла')

def test_info_about_system():
    auth = ('root', '0penBmc')
    url = "https://localhost:2443/redfish/v1/Systems/system"
    response = requests.get(url,auth=auth, verify=False)
    try:
        assert response.status_code == 200
        assert "Status" in response.json()
        assert "PowerState" in response.json()
    except Exception:
        print("Какая то из проверок не прошла")

def test_power_management(get_auth_token):
    try:
        assert get_auth_token.status_code == 201
    except Exception:
        print("Статус код не 201")
    url_power = "https://localhost:2443/redfish/v1/Systems/system/Actions/ComputerSystem.Reset"
    response_power = requests.post(url_power, json={"ResetType": "PowerOn"},
                                   headers={"Content-Type": "application/json",
                                            "X-Auth-Token": get_auth_token.headers['X-Auth-Token']},
                                   verify=False)
    try:
        assert response_power.status_code == 204
    except Exception:
        print("Неизвестная причина по которой статус код не 204")
    response_info_power = requests.get("https://localhost:2443/redfish/v1/Systems/system",
                            headers={"X-Auth-Token": get_auth_token.headers['X-Auth-Token']},
                              verify=False)
    try:
        assert response_info_power.json()["PowerState"] == "On"
    except Exception:
        print("Неизвестная причина по которой питание не включилась")






