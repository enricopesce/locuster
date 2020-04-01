from locust import HttpLocust, TaskSet, task, between

class UserTasks(TaskSet):
    @task
    def index(self):
        self.client.get("/")


class WebsiteUser(HttpLocust):
    wait_time = between(2, 5)
    task_set = UserTasks