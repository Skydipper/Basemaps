"""API ROUTER"""
import logging
import json
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
    try:
        if map_object is None:
            logging.info('Generating mapid')
            layer_config = layer_obj.get('layerConfig')
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
    return redirect(url)
