"""MIDDLEWARE"""
from flask import request, redirect
from functools import wraps
import logging
import requests
from basemaps.errors import LayerNotFound
from basemaps.routes.api import error
from basemaps.services.redis_service import RedisService


def exist_tile(func):
    """."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        url = RedisService.get(request.path)
        logging.info(f"[MIDDLEWARE exist_tile] {url}")
        if url is None:
            return func(*args, **kwargs)
        else:
            return redirect(url)
    return wrapper


def exist_mapid(func):
    """."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        year = kwargs['year']
        kwargs["map_object"] = RedisService.check_year_mapid(year)
        return func(*args, **kwargs)
    return wrapper


def get_layer(func):
    """."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            layer = kwargs['layer']
            #logging.info(f'[MIDDLEWARE get_layer] Getting layer: {layer}')
            url = f"https://api.skydipper.com/v1/layer/{layer}"
            r = requests.get(url)
            if r.status_code == 200:
                kwargs["layer_obj"] = r.json().get('data').get('attributes')
                return func(*args, **kwargs)
        except LayerNotFound as e:
            return error(status=404, detail=e.message)
        except Exception as e:
            return error(detail='Generic error')
    return wrapper
