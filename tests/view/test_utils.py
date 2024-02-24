from werkzeug.test import TestResponse

from easy_framework.view import GenericApiView
from easy_framework.view import register_view
from easy_framework._context import cache
from tests import TestCase

class TestUtils(TestCase):
    def setUp(self) -> None:
        super().setUp()
        self.app = cache.app
        register_view(self.View)
        register_view(self.View2, cache.app)

    def make_request(self, view: GenericApiView=None, route:int = 0)-> TestResponse:
        if not view:
            view = self.View

        route_to_request = view.routes[route]
        return self.app.test_client().get(route_to_request)    
    
    class View(GenericApiView):
        routes = ['/testViewUtils', '/testViewUtils2']
        methods = ['GET']
        model = None
        serializer = None
        field_lookup = None
        auto_treat_request = False

        def __init__(self):
            pass

        def get(self):
            return 'hello'
        
    class View2(View):
        routes = ['/testView2Utils', '/testView2Utils2']

        def get(self):
            return 'hello2'

    def test_make_request_to_view_1_route_0(self):
        res = self.make_request()
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_data(), b'hello')

    def test_make_request_to_view_1_route_1(self):
        res = self.make_request(route=1)
        self.assertEqual(res.status_code,  200)
        self.assertEqual(res.get_data(), b'hello')

    def test_make_request_to_view_2_route_0(self):
        res = self.make_request(self.View2)
        self.assertEqual(res.status_code,  200)
        self.assertEqual(res.get_data(), b'hello2')

    def test_make_request_to_view_2_route_1(self):
        res = self.make_request(self.View2, 1)
        self.assertEqual(res.status_code,  200)
        self.assertEqual(res.get_data(), b'hello2')