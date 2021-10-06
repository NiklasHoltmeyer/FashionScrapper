from time import sleep

from default_logger.defaultLogger import defaultLogger
from fashionscrapper.brand.asos.consts.parser import excludes, CATEGORIES
from fashionscrapper.brand.asos.webelements.AsosWebElements import AsosWebElements
from fashionscrapper.brand.generic import flatten_category
from fashionscrapper.utils.list import includes_excludes_filter


class Asos:
    def __init__(self, driver, logger=None):
        self.driver = driver
        self.logger = logger if logger else defaultLogger("Asos")

        self.elements = AsosWebElements(driver, self.logger)

    def list_categories(self, retries=3):
        categories = self.elements.categories.list_categories()
        if len(categories) == 0 and retries > 0:
            sleep(0.5)
            return self.list_categories((retries - 1))
        return categories

    def list_categories_group_by_name(self):
        categories = self.list_categories()

        filter_category = lambda category: (category["name"], [x for x in categories if
                                                               includes_excludes_filter(x["url"],
                                                                                        includes=category["includes"],
                                                                                        excludes=excludes)])
        filtered_categories = map(filter_category, CATEGORIES)
        filtered_categories = map(flatten_category, filtered_categories)
        return list(filtered_categories)

    def list_category(self, url, retries=2, PAGINATE=True):
        category = self.elements.category.list_category(url, PAGINATE=PAGINATE)
        if len(category) == 0 and retries > 0:
            sleep(0.5)
            return self.list_category(url, (retries - 1))
        return category

    def show(self, url):
        return self.elements.article.show(url)
