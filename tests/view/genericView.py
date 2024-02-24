from easy_framework.view import GenericApiView

class View(GenericApiView):
    routes = ['/testViewHandler', '/testViewHandler2']
    methods = ['GET']
    model = None
    serializer = None
    field_lookup = None
    auto_treat_request = False

    def __init__(self):
        pass

    def get(self):
        return 'hello_view_handler'