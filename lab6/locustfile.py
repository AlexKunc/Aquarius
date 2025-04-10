from locust import HttpUser, between, task

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

    @task
    def jsonplaceholder(self):
        self.client.get("https://jsonplaceholder.typicode.com/posts", verify=False)

    @task
    def weather(self):
        self.client.get("https://wttr.in/Novosibirsk?format=j1", verify=False)

