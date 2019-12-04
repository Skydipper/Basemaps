import logging
from basemaps.services.landsat_tiles import LandsatTiles

def test_LandsatTiles():
    """Test the Landsat Service."""
    l = LandsatTiles()
    assert l is not None
    return

