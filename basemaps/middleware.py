"""MIDDLEWARE"""
from flask import request, redirect
from functools import wraps
import logging
from basemaps.services.analysis.landsat_tiles_v1 import RedisService


def exist_tile(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = RedisService.get(request.path)
        if url is None:
            return func(*args, **kwargs)
        else:
            return redirect(url)
    return wrapper

def exist_mapid(func):
    """Get geodata"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        year = kwargs['year']
        kwargs["map_object"] = RedisService.check_year_mapid(year)
        return func(*args, **kwargs)
    return wrapper