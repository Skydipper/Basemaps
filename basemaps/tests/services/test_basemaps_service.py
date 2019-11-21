import logging
from basemaps.services.analysis.landsat_tiles import LandsatTiles

def test_LandsatTiles():
    """Test the Landsat Service."""
    l = LandsatTiles()
    assert l is not None