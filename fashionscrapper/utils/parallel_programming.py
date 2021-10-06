def calc_chunk_size(n_workers, len_iterable, factor=4):
    """
    SRC: https://stackoverflow.com/a/54032744
    Calculate chunksize argument for Pool-methods.

    Resembles source-code within `multiprocessing.pool.Pool._map_async`.
    """
    chunk_size, extra = divmod(len_iterable, n_workers * factor)

    if extra:
        chunk_size += 1
    return chunk_size
