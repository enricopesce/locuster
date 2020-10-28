from locusts import HeadlessChromeLocust
from locust import TaskSet, task


class LocustUserBehavior(TaskSet):

    def open_locust_homepage(self):
        self.client.get("https://www.pixartprinting.co.uk/")

    #def click_through_to_documentation(self):
    #    self.client.find_element_by_xpath('//a[text()="Documentation"]').click()
    #    self.client.wait.until(EC.visibility_of_element_located((By.XPATH, '//h1[text()="Locust Documentation"]')), "documentation is visible")

    @task(1)
    def homepage(self):
        self.client.timed_event_for_locust("Go to", "homepage", self.open_locust_homepage)
        #self.client.timed_event_for_locust("Click to", "documentation", self.click_through_to_documentation)


class LocustUser(HeadlessChromeLocust):
    host = "not really used"
    timeout = 30 #in seconds in waitUntil thingies
    min_wait = 100
    max_wait = 200
    screen_width = 1200
    screen_height = 600
    tasks = [LocustUserBehavior]
