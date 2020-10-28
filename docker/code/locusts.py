# pylint:disable=too-few-public-methods
""" Combine Locust with Selenium Web Driver """
import logging
import os 
from os import getenv as os_getenv
from locust import User
from locust.exception import LocustError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from core import RealBrowserClient
from sys import platform


dir_path = os.path.dirname(os.path.realpath(__file__))

_LOGGER = logging.getLogger(__name__)


class RealBrowserLocust(User):
    """
    This is the abstract Locust class which should be subclassed.
    """
    client = None
    timeout = 30
    screen_width = None
    screen_height = None
    abstract = True

    def __init__(self, parent):
        super().__init__(parent)
        if self.screen_width is None:
            raise LocustError("You must specify a screen_width "
                              "for the browser")
        if self.screen_height is None:
            raise LocustError("You must specify a screen_height "
                              "for the browser")
        self.proxy_server = os_getenv("LOCUST_BROWSER_PROXY", None)


class ChromeLocust(RealBrowserLocust):
    """
    Provides a Chrome webdriver that logs GET's and waits to locust
    """
    abstract = True

    def __init__(self, parent):
        super().__init__(parent)
        options = webdriver.ChromeOptions()
        if platform == "linux" or platform == "linux2":
            path = dir_path + "/linux"
        elif platform == "darwin":
            path = dir_path + "/mac"

        print(path + "/chromedriver")
        if self.proxy_server:
            _LOGGER.info('Using proxy: ' + self.proxy_server)
            options.add_argument('proxy-server={}'.format(self.proxy_server))
        self.client = RealBrowserClient(
            webdriver.Chrome(executable_path=path + "/chromedriver"),
            self.timeout,
            self.screen_width,
            self.screen_height
        )


class HeadlessChromeLocust(RealBrowserLocust):
    """
    Provides a headless Chrome webdriver that logs GET's and waits to locust
    """
    abstract = True

    def __init__(self, parent):
        super().__init__(parent)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument('window-size={}x{}'.format(
            self.screen_width, self.screen_height
        ))
        options.add_argument('disable-gpu')
        if self.proxy_server:
            _LOGGER.info('Using proxy: ' + self.proxy_server)
            options.add_argument('proxy-server={}'.format(self.proxy_server))
        driver = webdriver.Chrome(chrome_options=options)
        _LOGGER.info('Actually trying to run headless Chrome')
        self.client = RealBrowserClient(
            driver,
            self.timeout,
            self.screen_width,
            self.screen_height,
            set_window=False
        )


class FirefoxLocust(RealBrowserLocust):
    """
    Provides a Firefox webdriver that logs GET's and waits to locust
    """
    abstract = True
    def __init__(self, parent):
        super().__init__(parent)
        self.client = RealBrowserClient(
            webdriver.Firefox(),
            self.timeout,
            self.screen_width,
            self.screen_height
        )


class PhantomJSLocust(RealBrowserLocust):
    """
    Provides a PhantomJS webdriver that logs GET's and waits to locust
    """
    abstract = True
    def __init__(self, parent):
        super().__init__(parent)
        self.client = RealBrowserClient(
            webdriver.PhantomJS(),
            self.timeout,
            self.screen_width,
            self.screen_height
        )
