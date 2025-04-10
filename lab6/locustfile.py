from locust import HttpUser, between, task
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

class OpenBMC(HttpUser):
    wait_time = between(1,5)
    host = "https://localhost:2443"

    @task
    def auth_open_bmc(self):
        self.client.get("/redfish/v1/SessionService/Sessions", auth=("root", "0penBmc"), verify=False)

    @task
    def info_open_bmc(self):
        self.client.get("/redfish/v1/Systems/system", auth=("root", "0penBmc"), verify=False)

class PublicAPI(HttpUser):
    wait_time = between(1,2)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def jsonplaceholder(self):
        self.client.get("/posts")

    @task
    def weather(self):
        self.client.get("https://wttr.in/Novosibirsk?format=j1", verify=False)

