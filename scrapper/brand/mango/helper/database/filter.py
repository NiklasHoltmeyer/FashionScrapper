from random import sample

from scrapper.brand.mango.helper.download.MangoPaths import MangoPaths


def filtered_entries(entries, shuffle_images=True):
    """
    Filter Entries>Images by View
    """
    # noinspection SpellCheckingInspection
    views_filter = ['Mittlere Ansicht', 'Allgemeine Ansicht', 'Rückseite des Artikels', 'Artikel ohne Model']
    for entry in entries:
        _id, images = MangoPaths.relative_url(entry["url"]), entry["images"]
        images_filtered = [{"view": x["description"], "path": x["path"]} for x in images if
                          x["description"] in views_filter]
        if shuffle_images:
            yield {"id": _id, "images": sample(images_filtered, len(images_filtered))}
        else:
            yield {"id": _id, "images": images_filtered}


