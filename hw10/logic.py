import os
from flask import abort, url_for
import pathlib as pth
import random


class Application:
    page_title = "Cat of the day!"
    CATDIR = './static/cats/'
    _PROJDIR = pth.Path(__file__).parent

    @classmethod
    def get_cats(cls):
        # Ensure all directories reside under project directory
        # and are resolved relative to it

        catdir = cls._PROJDIR.joinpath(pth.Path(cls.CATDIR))
        assert catdir.is_relative_to(cls._PROJDIR)
        cats = tuple(catdir.iterdir())
        return cats

    @classmethod
    def get_cat_urls(cls):
        return [url_for('get_cat_image', filename=os.path.basename(path)) for path in Application.get_cats()]

    @classmethod
    def get_cat_url_by_name(cls, name):
        return url_for('get_cat_image', filename=os.path.basename(cls.find_cat_file_by_name(name)))

    @classmethod
    def get_cat(cls, numext, try_random=False):
        try:
            ret = cls.find_cat_file_by_num(numext=numext, try_random=try_random)
        except ValueError:  # integer unconvertable or wrong range
            abort(404, 'Wrong image number')
        else:
            return ret

    @classmethod
    def get_cat_count(cls):
        return len(cls.get_cats())

    @classmethod
    def find_cat_file_by_num(cls, numext, try_random=False):
        p = pth.Path(numext)
        base, ext = (p.stem, p.suffix) if p.suffix else ('', numext)

        # num specifies the cat image to use
        # if num is omitted, and try_random is True, random cat should appear
        if try_random is True and not base:
            num = random.randint(0, cls.get_cat_count() - 1)
        else:
            num = int(base)  # try integer conversion

        if num < 0 or num > cls.get_cat_count() - 1:
            raise ValueError

        return cls.get_cats()[num], base, ext

    @classmethod
    def find_cat_file_by_name(cls, cat_name: str) -> pth.PosixPath:
        for cat_file in cls.get_cats():
            if cat_file.name == cat_name:
                return cat_file
        raise ValueError(f"Could not find cat file with name {cat_name}")
