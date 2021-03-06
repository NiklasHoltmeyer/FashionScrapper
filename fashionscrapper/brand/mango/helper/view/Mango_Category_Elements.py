import time

from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from fashionscrapper.utils.web.dynamic import wait, scroll_end_of_page


class Mango_Category_Elements:
    """ List all Links/Images withing an Category (e.g. T-Shirts) """

    def __init__(self, web_elements):
        self.elements = web_elements
        self.driver = web_elements.driver
        self.logger = web_elements.logger

    def load_html(self, url, timeout=1.5):
        self.driver.get(url)

        try:
            wait(self.driver, EC.presence_of_element_located((By.ID, 'app')))
        except TimeoutException as e:
            raise Exception({"exception" : e, "function":"mango_category_elements.load_html", "url": url})

        self.elements.accept_cookies()

        last_article_count = -1

        while True:  # Scroll as Long as new Content is Loaded
            scroll_end_of_page(self.driver, SCROLL_TOP=True)

            catalog = self.driver.find_elements_by_css_selector("#app>.catalog")
            catalog_flattened = "\n".join([x.get_attribute('innerHTML') for x in catalog])

            if last_article_count == len(catalog_flattened):
                return catalog_flattened
            else:
                last_article_count = len(catalog_flattened)
                time.sleep(timeout)

    def list_images(self, url):
        self.logger.debug(f"Loading: {url}")

        html = self.load_html(url)

        doc = BeautifulSoup(html, "html.parser")
        article_imgs = doc.findAll("img", attrs={'class': 'product'})

        return article_imgs