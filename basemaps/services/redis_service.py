import ee
import json
import logging
import redis
from basemaps.config import SETTINGS


r = redis.StrictRedis.from_url(url=SETTINGS.get('redis').get('url'))

class RedisService(object):

    @staticmethod
    def check_year_mapid(year):
        text = r.get(year)
        if text is not None:
            return json.loads(text)
        return None

    @staticmethod
    def get(year):
        text = r.get(year)
        if text is not None:
            return text
        return None

    @staticmethod
    def set_year_mapid(year, mapid, token):
        return r.set(year, json.dumps({'mapid': mapid, 'token': token}), ex=2 * 24 * 60 * 60)

    @staticmethod
    def check_layer_mapid(layer):
        text = r.get(layer)
        if text is not None:
            return json.loads(text)
        return None

    @staticmethod
    def set(key, value):
        return r.set(key, value)

    @staticmethod
    def expire_layer(layer):
        for key in r.scan_iter("*"+layer+"*"):
            r.delete(key)

    @staticmethod
    def set_layer_mapid(layer, mapid, token):
        return r.set(layer, json.dumps({'mapid': mapid, 'token': token}), ex=2 * 24 * 60 * 60)
