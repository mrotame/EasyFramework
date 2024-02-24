from abc import ABC
from flask.views import View as FlaskView

class GenericApiViewMeta(type(ABC), type(FlaskView)):
    '''
    Meta class for the inheritance
    '''
    pass