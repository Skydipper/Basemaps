"""VALIDATORS"""

from flask import request
from functools import wraps
from basemaps.routes.api import error


def validate_landsat_year(func):
    """Landsat Years Validation"""

    @wraps(func)
    def wrapper(*args, **kwargs):
        years = ['2012', '2013', '2014', '2015', '2016', '2017']
        year = kwargs['year']
        if year not in years:
            return error(status=400, detail='Year is not valid')
        return func(*args, **kwargs)

    return wrapper
