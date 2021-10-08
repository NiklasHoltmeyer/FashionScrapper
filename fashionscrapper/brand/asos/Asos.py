from time import sleep

from fashionscrapper.brand.asos.helper.database.dbhelper import list_dbs_by_category
from fashionscrapper.brand.asos.helper.download.AsosPaths import AsosPaths
from fashionscrapper.brand.asos.webelements.consts.Asos_Selectors import Asos_Selectors
from fashionscrapper.default_logger.defaultLogger import defaultLogger
from fashionscrapper.brand.asos.consts.parser import excludes, CATEGORIES, BASE_PATH
from fashionscrapper.brand.asos.webelements.AsosWebElements import AsosWebElements
from fashionscrapper.brand.generic import flatten_category
from fashionscrapper.utils.io import Json_DB
from fashionscrapper.utils.list import includes_excludes_filter, distinct_list_of_dicts, flatten


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

    @staticmethod
    def list_entries_from_category_name(category_name, filter_views=True, clean_entries=True):
        brand_path = AsosPaths(BASE_PATH)

        def clean_entry(entry):
            return {"id": entry["url"].replace(Asos_Selectors.URLS.BASE, ""),
                    "images": [{"path": brand_path.relative_image_path_from_url(img["url"]), "view": img["name"]}
                               for img in entry["images"]]}

        entries_db_path = brand_path.get_entries_db_base_path()
        entries = list_dbs_by_category(entries_db_path, CATEGORIES)
        entries_by_cat_distinct = distinct_list_of_dicts(flatten([Json_DB(x).all() for x in entries[category_name]]),
                                                         key="url")
        if clean_entries:
            return map(clean_entry, entries_by_cat_distinct)
        return entries_by_cat_distinct

    @staticmethod
    def list_entries_by_category_name(filter_views=True, clean_entries=True):
        cat_names = map(lambda d: d["name"], CATEGORIES)
        lst_entries = lambda name: Asos.list_entries_from_category_name(name, filter_views=filter_views,
                                                                        clean_entries=clean_entries)
        lst_entries_w_name = lambda name: (name, lst_entries(name))
        return map(lst_entries_w_name, cat_names)

    @staticmethod
    def name():
        return "Asos"

    @staticmethod
    def image_url_key():
        return "url"

    @staticmethod
    def absolute_image_path_fn():
        return lambda URL: AsosPaths(BASE_PATH).relative_image_path_from_url(URL, False)

    @staticmethod
    def view_blacklist():
        return []


