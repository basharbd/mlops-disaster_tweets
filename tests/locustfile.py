from locust import HttpUser, task, between

class DisasterTweetUser(HttpUser):
    # Wait between 1 and 5 seconds between tasks (simulates a real human)
    wait_time = between(1, 5)

    @task
    def predict_disaster(self):
        # Send a fake disaster tweet
        self.client.post("/predict", json={
            "text": "Huge fire in the forest! Everyone is running."
        })

    @task
    def predict_safe(self):
        # Send a fake normal tweet
        self.client.post("/predict", json={
            "text": "Just enjoying the sunny weather."
        })

    @task
    def visit_root(self):
        # Visit the welcome page
        self.client.get("/")
