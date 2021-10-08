from multiprocessing.dummy import freeze_support, Pool
from pathlib import Path

from fashionscrapper.brand.asos.Asos import Asos
from fashionscrapper.brand.hm.HM import HM
from fashionscrapper.brand.mango.Mango import Mango
from fashionscrapper.brand.parser_settings import BASE_PATH
from fashionscrapper.default_logger.defaultLogger import defaultLogger
from fashionscrapper.utils.io import Json_DB
from fashionscrapper.utils.list import filter_not_none


def walk_entries(brands):
    def clean_entry(entry, path_fn, brand_name, category, url_key, bl):
        is_mango = brand_name == Mango.name()

        def clean_image(img, validate=True):
            description = img.pop("description", "")
            if description in bl:
                return None
            path_str = path_fn(img[url_key]) if not is_mango else path_fn(img[url_key], category)
            path_str = str(path_str)
            if validate and not Path(path_str).exists():
                print(entry)
                print(path_str)
                exit(0)

            return {"path": path_str, "description": description}

        entry["images"] = list(filter_not_none(map(clean_image, entry["images"])))
        entry["brand"] = brand_name
        entry["category"] = category
        return entry

    for brand in brands:
        brand_name = brand.name()
        brand_url_key = brand.image_url_key()
        relative_image_path_fn = brand.absolute_image_path_fn()
        bl = brand.view_blacklist()
        cat_entries = brand.list_entries_by_category_name(filter_views=False, clean_entries=False)

        for cat_name, cat_entries in cat_entries:
            for entry in cat_entries:
                yield clean_entry(entry, relative_image_path_fn, brand_name, cat_name, brand_url_key, bl)


def entries_to_json(brands, entries_path, force=False):
    entries_path = Path(entries_path)

    if force:
        entries_path.unlink()

    if not entries_path.exists():
        entries = list(walk_entries(brands))

        with Json_DB(entries_path) as db:
            db.insert_multiple(entries)

    with Json_DB(entries_path) as db:
        return db.all()


if __name__ == "__main__":
    entries_path = Path(BASE_PATH, "entires.json")

    brands = [Asos, Mango, HM]

    entries = entries_to_json(brands, entries_path, force=False)
    print(len(entries))
