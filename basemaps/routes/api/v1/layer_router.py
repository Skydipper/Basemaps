"""API ROUTER"""
import logging
import json
import urllib
import requests
from flask import jsonify, Blueprint, redirect, request
from basemaps.routes.api import error
from basemaps.middleware import exist_mapid, get_layer, exist_tile
from basemaps.services.redis_service import RedisService
import ee


layer_endpoints = Blueprint('tile_endpoints', __name__)

@layer_endpoints.route('/<layer>/<z>/<x>/<y>', strict_slashes=False, methods=['GET'])
@get_layer
def get_tile(layer, z, x, y, map_object=None, layer_obj=None):
    """Get tile Endpoint"""
    #logging.info(f"[Layer Router]: made it to router. {z}/{x}/{y}")
    try:
        layer_config = layer_obj.get('layerConfig')
        layer_type = layer_obj.get('provider')
    except Exception as e:
        logging.error(str(e))
        return error(status=500, detail='Error grabbing layer data: ' + str(e))
    # IF Carto type of layer
    if layer_type == 'cartodb':
        #logging.info(f"[Layer Router] Carto type: {layer_type}")
        tmp_url = get_carto_url(layer_config)
        url = tmp_url.replace("{z}/{x}/{y}", f"{z}/{x}/{y}")
        #logging.info(f"[Layer Router]: URL.{url}")
    # IF EE type of layer
    if layer_type == 'gee':
        #logging.info(f"[Layer Router] EE type: {layer_type}")
        try:
            if map_object is None:
                logging.info('Generating mapid')
                style_type = layer_config.get('body').get('styleType')
                image = None
                if 'isImageCollection' not in layer_config or not layer_config.get('isImageCollection'):
                    image = ee.Image(layer_config.get('assetId'))
                else:
                    position = layer_config.get('position')
                    image_col = ee.ImageCollection(layer_config.get('assetId'))
                    if 'filterDates' in layer_config:
                        dates = layer_config.get('filterDates')
                        image_col = image_col.filterDate(dates[0], dates[1])
                    if position == 'first':
                        logging.info('Obtaining first')
                        image = ee.Image(image_col.sort('system:time_start', True).first())
                    else:
                        logging.info('Obtaining last')
                        image = ee.Image(image_col.sort('system:time_start', False).first())
                if style_type == 'sld':
                    style = layer_config.get('body').get('sldValue')
                    map_object = image.sldStyle(style).getMapId()
                else:
                    map_object = image.getMapId(layer_config.get('body'))
                RedisService.set_layer_mapid(layer, map_object.get('mapid'), map_object.get('token'))
        except Exception as e:
            logging.error(str(e))
            return error(status=500, detail='Error generating tile: ' + str(e))
        try:
            url = ee.data.getTileUrl(map_object, int(x), int(y), int(z))
        except Exception as e:
            logging.error(str(e))
            return error(status=404, detail='Tile Not Found')
    # Return back the url of the individual tile either from EE or Carto
    return redirect(url)


def get_carto_url(layerConfig):
    """blah"""
    sql_config = layerConfig.get('sql_config', None)
    if sql_config:
        for config in sql_config:
            logging.info(f"[Layer Router] SQL: {config}")
            key = config['key']
            key_params = config['key_params']
            if key_params[0].get('required', False):
                for l in layerConfig["body"]["layers"]:
                    l['options']['sql'] = l['options']['sql'].replace(f'{{{key}}}', '0').format(key_params['key'])
            else:
                for l in layerConfig["body"]["layers"]:
                    l['options']['sql'] = l['options']['sql'].replace(f'{{{key}}}', '0').format('')
    _layerTpl = urllib.parse.quote_plus(json.dumps({
        "version": "1.3.0",
        "stat_tag": "API",
        "layers": [{ **l, "options": { **l["options"]}} for l in layerConfig.get("body").get("layers")]
    }))
    apiParams = f"?stat_tag=API&config={_layerTpl}"
    url = f"http://35.233.41.65/user/skydipper/api/v1/map{apiParams}"
    r = requests.get(url, headers={'Content-Type': 'application/json'})
    try:
        tile_url = r.json().get('metadata').get('tilejson').get('raster').get('tiles')[0]
        return tile_url
    except:
        return None