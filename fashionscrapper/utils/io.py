import json
import time
from functools import wraps
from math import ceil
from pathlib import Path

from tinydb import TinyDB
from tinydb.middlewares import CachingMiddleware
from tinydb.storages import JSONStorage
from tinydb_serialization import SerializationMiddleware
from tinydb_serialization.serializers import DateTimeSerializer

from fashionscrapper.default_logger.defaultLogger import defaultLogger


def Json_DB(*paths):
    serializationMiddleware = SerializationMiddleware(JSONStorage)
    serializationMiddleware.register_serializer(DateTimeSerializer(), 'TinyDate')

    storage = (CachingMiddleware(serializationMiddleware))

    return TinyDB(Path(*paths), storage=storage)


def list_json_dbs(path, BLACKLIST=None):
    BLACKLIST = BLACKLIST if BLACKLIST else ["visited.json"]

    _blacklist_filter = lambda x: len([bl for bl in BLACKLIST if bl in str(x)]) == 0
    return [x for x in Path(path).rglob('*.json') if _blacklist_filter(x)]


def walk_entries(path, BLACKLIST=None):
    db_iter = list_json_dbs(path, BLACKLIST=BLACKLIST) if BLACKLIST else list_json_dbs(path)
    for db_path in db_iter:
        with Json_DB(db_path) as db:
            for entry in db.all():
                yield entry


def time_logger(**kwargs):
    logger = kwargs.get("logger", defaultLogger("Fashion Scrapper"))
    log_debug = kwargs.get("log_debug", True)

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **inner_kwargs):
            startTime = time.time()
            name = kwargs.get("name", func.__name__)
            header = kwargs.get("header", None)
            footer = kwargs.get("footer", None)

            if header:
                header_msg = pad_str(header, **kwargs)
                if log_debug:
                    logger.debug(header_msg, extra={'name_override': func.__name__})
                else:
                    logger.info(header_msg, extra={'name_override': func.__name__})

            result = func(*args, **inner_kwargs)

            totalTime = time.time() - startTime

            if log_debug:
                logger.debug(f"[{name}] Elapsed Time: {totalTime}s", extra={'name_override': func.__name__})
            else:
                logger.info(f"[{name}] Elapsed Time: {totalTime}s", extra={'name_override': func.__name__})

            if footer:
                footer_msg = pad_str(footer, **kwargs)
                if log_debug:
                    logger.debug(footer_msg, extra={'name_override': func.__name__})
                else:
                    logger.info(footer_msg, extra={'name_override': func.__name__})
            return result

        return wrapper

    return decorator


def pad_str(msg, **kwargs):
    length = kwargs.get("padding_length", 32)
    symbol = kwargs.get("padding_symbol", "*")

    symbol_count = ceil((length - len(msg)) / 2) - 1

    symbols = symbol * symbol_count
    return f"{symbols} {msg} {symbols}"


def json_load(file_path):
    with open(file_path, ) as f:
        data = json.load(f)
        return data