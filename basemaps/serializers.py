"""Serializers"""
import logging




def serialize_composite_output(analysis, type):
    """."""
    return {
        'id': None,
        'type': type,
        'attributes': {
            'thumb_url': analysis.get('thumb_url', None),
            'tile_url':analysis.get('tile_url', None),
            'dem':analysis.get('dem', None),
            'zonal_stats':analysis.get('zonal_stats', None)
        }
    }


def serialize_landsat_url(analysis, type):
    """Convert output of landsat_tiles to json"""
    return {
        'id': None,
        'type': type,
        'attributes': {
            "url": analysis.get('url', None)
        }
    }


def serialize_sentinel_url(analysis, type):
    """Convert output of landsat_tiles to json"""
    return {
        'id': None,
        'type': type,
        'attributes': {
            "url_image": analysis.get('image_tiles', None),
            "url_boundary": analysis.get('boundary_tiles', None),
            "date_time": analysis.get('metadata', None).get('date_time', None),
            "product_id": analysis.get('metadata', None).get('product_id', None)
        }
    }

def serialize_sentinel_mosaic(analysis, type):
    """Convert output of landsat_tiles to json"""
    return {
        'id': None,
        'type': type,
        'attributes': {
            "tile_url": analysis.get('tile_url', None),
            "thumbnail_url": analysis.get('thumb_url', None),
            "bbox": analysis.get('bbox', None),
        }
    }

def serialize_highres_url(analysis, type):
    """Convert output of images to json"""
    output = []

    for e in range(0, len(analysis)):
        temp_output = {
            'id': None,
            'type': type,
            'attributes': {
                'source': analysis[e].get('metadata', None).get('source', None),
                'cloud_score': analysis[e].get('metadata', None).get('cloud_score', None),
                'date_time': analysis[e].get('metadata', None).get('date_time', None),
                'metadata': analysis[e].get('metadata', None),
                'tile_url': analysis[e].get('tile_url', None),
                'thumbnail_url': analysis[e].get('thumbnail_url', None),
                'boundary_tiles': analysis[e].get('boundary_tiles', None)
            }
        }
        output.append(temp_output)

    return output


def serialize_recent_data(analysis, type):
    logging.info("[SERIALISER] initiating...")
    """Convert output of images to json"""
    output = []

    for e in range(0, len(analysis)):
        temp_output = {
            'attributes': {
                'instrument': analysis[e].get('spacecraft', None),
                'source': analysis[e].get('source', None),
                'cloud_score': analysis[e].get('cloud_score', None),
                'date_time': analysis[e].get('date', None),
                'tile_url': analysis[e].get('tile_url', None),
                'thumbnail_url': analysis[e].get('thumb_url', None),
                'bbox': analysis[e].get('bbox', None)
            }
        }
        output.append(temp_output)
    return {
        'tiles': output,
        'id': None,
        'type': type
    }