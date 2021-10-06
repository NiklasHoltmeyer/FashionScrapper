def flatten_category(category):
    cat_name, cat_data = category
    cat_urls = [x["url"] for x in cat_data]
    return list(zip([cat_name] * len(cat_urls), cat_urls))