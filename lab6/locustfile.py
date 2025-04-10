from locust import HttpUser, between, task

class OpenBMC(HttpUser):
    wait_time = between(1,5)
    host = "https://localhost:2443/redfish/v1"

    @task
    def auth_open_bmc(self):
        self.client.get("/SessionService/Sessions", auth=("root", "0penBmc"), verify=False)

    @task
    def info_open_bmc(self):
        self.client.get("/Systems/system", auth=("root", "0penBmc"), verify=False)

class PublicAPI(HttpUser):
    wait_time = between(1,2)
    host = "https://jsonplaceholder.typicode.com"

    @task
    def jsonplaceholder(self):
        self.client.get("/posts")

    @task
    def weather(self):
        self.client.get("https://wttr.in/Novosibirsk?format=j1", verify=False)

