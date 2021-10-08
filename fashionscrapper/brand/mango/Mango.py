import os
from pathlib import Path
from time import sleep
from urllib.parse import urlparse

from fashionscrapper.brand.mango.consts.parser import BASE_PATH, CATEGORIES, view_blacklist as view_bl
from fashionscrapper.brand.mango.helper.database.filter import filtered_entries
from fashionscrapper.brand.mango.helper.download.MangoPaths import MangoPaths
from fashionscrapper.default_logger.defaultLogger import defaultLogger
from fashionscrapper.brand.mango.webelements.MangoWebElements import MangoWebElements
from fashionscrapper.utils.io import walk_entries
from fashionscrapper.utils.web.static import find_first_parent_href


class Mango:
    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger if logger else defaultLogger("Mongo")

        self.elements = MangoWebElements(driver, self.logger)

    def list_categories(self, url, retries=2):
        categories = [x["href"] for x in self.elements.categories.list_categories(url)]
        distinct_links = list(dict.fromkeys(sorted(categories)))
        _filter_top_level_categories = lambda x: len(x.split("/")) > 5
        categories = [x for x in distinct_links if _filter_top_level_categories(x)]

        if len(categories) == 0 and retries > 0:
            sleep(0.5)
            return self.list_categories(url, (retries - 1))

        return categories

    def list_category(self, url, retries=2):
        def parse_preview_images(preview_img):
            img_info = preview_img.attrs
            article_url = find_first_parent_href(preview_img)
            article_url = urlparse(article_url).path  # removing fragments / queries / ...

            img_info["url"] = f"{self.elements.selectors.URLS.BASE_FULL}/{article_url}".replace("//", "/")

            return img_info

        # -> List all Links withing an Category (T-Shirts)
        article_imgs = self.elements.category.list_images(url)

        articles = [parse_preview_images(x) for x in article_imgs]
        articles = list({x['url']: x for x in articles}.values())  # remove duplications (based on url)

        if len(articles) == 0 and retries > 0:
            sleep(0.5)
            return self.list_category(url, (retries - 1))

        return articles

    def show(self, url):
        return self.elements.article.show(url)

    @staticmethod
    def list_entries_from_category_name(category_name, filter_views=True, clean_entries=True):
        entries = walk_entries(rf"{BASE_PATH}\{category_name}")
        if filter_views:
            return filtered_entries(entries)
        return entries

    @staticmethod
    def list_entries_by_category_name(filter_views=True, clean_entries=True):
        cat_names = map(lambda d: d["name"], CATEGORIES)

        lst_entries = lambda name: Mango.list_entries_from_category_name(name, filter_views=filter_views,
                                                                         clean_entries=clean_entries)
        lst_entries_w_name = lambda name: (name, lst_entries(name))

        cat_entries = map(lst_entries_w_name, cat_names)
        return cat_entries

    @staticmethod
    def name():
        return "Mango"

    @staticmethod
    def image_url_key():
        return "src"

    @staticmethod
    def absolute_image_path_fn():
        paths = MangoPaths(BASE_PATH)
        def __call__(URL, category):
            relative_path = paths.relative_img_real_path(URL)

            return Path(BASE_PATH + "/" + category + "/" + relative_path)
        return __call__

    @staticmethod
    def view_blacklist():
        return view_bl


if __name__ == "__main__":
    from selenium.webdriver import Chrome


    def _categories(mango, url="https://shop.mango.com/de/herren"):
        categories = mango.list_categories(url)

        print("*" * 8, "Categories", "*" * 8)
        print(categories)
        print("-" * len("*" * 8 + "Categories" + "*" * 8))
        print("Len(Cat)", len(categories))
        print("*" * len("*" * 8 + "Categories" + "*" * 8))


    def _category(mango, url="https://shop.mango.com/de/herren/t-shirts_c12018147"):
        category = mango.list_category(url)

        print("*" * 9, "Category", "*" * 9)
        print(category)
        print("-" * len("*" * 9 + "Category" + "*" * 9))
        print("Len(Cat)", len(category))
        print("*" * len("*" * 9 + "Category" + "*" * 9))


    def _item(mango, url="https://shop.mango.com/de/herren/t-shirts-unifarben/meliertes-strick-t-shirt_17010542.html"):
        item = mango.show(url)

        print("*" * 11, "Item", "*" * 11)
        print(item)
        # print("-"*len("*"*11 + "Item" + "*"*11))
        # print("Len(Cat)", len(Item))
        print("*" * len("*" * 11 + "Item" + "*" * 11))


    with Chrome("C:\selenium\chromedriver.exe") as driver:
        driver.maximize_window()
        mango = Mango(driver)

        # _categories(mango=mango)
        # _category(mango=mango)
        _item(mango=mango)
