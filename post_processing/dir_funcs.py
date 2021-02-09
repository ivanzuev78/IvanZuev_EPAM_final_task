import os
from contextlib import contextmanager


@contextmanager
def chdir_to_country_city(*args):
    start_dir = os.getcwd()
    try:
        for directory in args:
            if not os.path.isdir(directory):
                os.mkdir(directory)
            os.chdir(directory)
        yield
    finally:
        os.chdir(start_dir)
