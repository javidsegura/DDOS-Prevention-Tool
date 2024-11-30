""" Check this out: https://www.cloudflare.com/learning/ddos/syn-flood-ddos-attack/ """

from locust import HttpUser, task, between

class StreamlitUser(HttpUser):
    wait_time = between(0.1, 1)  # Reduced wait time for more frequent requests
    
    @task
    def load_homepage(self):
        self.client.get("/")

