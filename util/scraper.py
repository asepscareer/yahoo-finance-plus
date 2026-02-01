import os
from io import StringIO

import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class TableScraper:
    def __init__(self, url):
        self.url = url
        self.options = self._get_chrome_options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def _get_chrome_options(self) -> Options:
        options = Options()
        options.add_argument(
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")
        options.add_argument("start-maximized")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("--disable-infobars")
        options.add_argument("--disable-extensions")
        options.add_argument("--headless")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        options.add_argument('--single-process')
        options.add_argument('--disable-gpu')
        options.add_argument('--remote-debugging-port=9222')
        options.add_argument('--disable-browser-side-navigation')
        options.add_argument("--example-flag")
        options.add_argument('--blink-settings=imagesEnabled=false')
        options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
        return options

    def get_data(self):
        content = None
        try:
            self.driver.get(self.url)
            html = self.driver.page_source
            html_stringio = StringIO(html)
            content = pd.read_html(html_stringio)
        except Exception as e:
            print(str(e))
        finally:
            self.driver.quit()
        return content
