"""ERRORS"""


class Error(Exception):

    def __init__(self, message):
        self.message = message

    @property
    def serialize(self):
        return {
            'message': self.message
        }


class LandsatTilesError(Error):
    pass

class LayerNotFound(Error):
    pass
