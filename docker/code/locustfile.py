import random
import re

from bs4 import BeautifulSoup
from locust import HttpUser, SequentialTaskSet, task, constant, tag


class RandomWalk(SequentialTaskSet):
    index_urls = []
    subpage_urls = []

    def on_start(self):
        # self.client.verify = False
        self.cookies = {
            'example': 'abc'}

    def load_random_page(self):
        url = random.choice(self.index_urls)
        r = self.client.get(url, cookies=self.cookies).text
        bs = BeautifulSoup(r, "html.parser")
        hrefs = bs.findAll('a', attrs={'href': re.compile("^/")})
        self.index_urls = [
            href.get('href') for href in hrefs
        ]

    @tag('LoadHome')
    @task
    def home(self):
        r = self.client.get("/", cookies=self.cookies).text
        bs = BeautifulSoup(r, "html.parser")
        hrefs = bs.findAll('a', attrs={'href': re.compile("^/.")})
        self.index_urls = [
            href.get('href') for href in hrefs
        ]

    @tag('LoadFirstRandom')
    @task
    def second_task(self):
        self.load_random_page()

    @tag('LoadSecondRandom')
    @task
    def third_task(self):
        self.load_random_page()

    @tag('LoadThirdRandom')
    @task
    def fourth_task(self):
        self.load_random_page()


class CustomerUser(HttpUser):
    wait_time = constant(1)
    tasks = [RandomWalk]
