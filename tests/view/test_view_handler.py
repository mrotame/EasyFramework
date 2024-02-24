import os
from pathlib import Path

from flask import Flask

from tests.view import genericView
from easy_framework.view._viewHandler import ViewHandler, FilterModules
from tests import TestCase

View = genericView.View
path = Path('/'.join(genericView.__file__.split('/')[:-1]))

class TestFilterModules(TestCase):
    files_in_this_directory = [i for i in os.listdir(path) if i[-3:] == '.py']

    def test_find_all_python_files_in_a_directory(self):
        py_file_list = FilterModules().find_all_python_files(path)

        self.assertEqual(len(py_file_list), len(self.files_in_this_directory))

    def test_remove_init_from_file_list(self):
        view_list = FilterModules().remove_init_from_file_list(self.files_in_this_directory)

        self.assertEqual(len(view_list), len(self.files_in_this_directory) -1)
        self.assertTrue('__init__.py' not in view_list)

    def test_convert_from_path_to_module(self):
        filter = FilterModules()
        file_list = filter.find_all_python_files(path)
        file_list = filter.remove_init_from_file_list(file_list)
        module_list = filter.convert_from_path_to_module(file_list)

        self.assertGreater(len(module_list), 0)
        self.assertEqual(len(module_list), len(file_list))

        for i in range(len(module_list)):
            set_module = set(module_list[i].split('.'))
            set_file = set([i.strip('.py') for i in Path(file_list[i]).parts])

            self.assertTrue(set_module.issubset(set_file))

    def test_get_modules(self):
        filter = FilterModules()
        file_list = filter.find_all_python_files(path)
        file_list = filter.remove_init_from_file_list(file_list)
        module_list = filter.getModules(path)

        self.assertGreater(len(module_list), 0)
        self.assertEqual(len(module_list), len(file_list))

        for i in range(len(module_list)):
            set_module = set(module_list[i].split('.'))
            set_file = set([i.strip('.py') for i in Path(file_list[i]).parts])

            self.assertTrue(set_module.issubset(set_file))

class TestViewHandler(TestCase):
    files_in_this_directory = [i for i in os.listdir(path) if i[-3:] == '.py']

    def test_get_modules(self):
        module_list = ViewHandler().get_modules(path)
        file_list = FilterModules().find_all_python_files(path)
        file_list = FilterModules().remove_init_from_file_list(file_list)

        self.assertGreater(len(module_list), 1)
        self.assertEqual(len(module_list), len(self.files_in_this_directory)-1)

        for i in range(len(module_list)):
            set_module = set(module_list[i].split('.'))
            set_file = set([i.strip('.py') for i in Path(file_list[i]).parts])

            self.assertTrue(set_module.issubset(set_file))

    def test_filter_views_from_module_list(self):
        module_list = ViewHandler().get_modules(path)
        view_list = ViewHandler().filter_views_from_module_list(module_list, View.__name__)

        self.assertTrue(View in view_list)

    def test_register_all_views(self):
        flaskApp = Flask(__name__)

        module_list = ViewHandler().get_modules(path)
        view_list = ViewHandler().filter_views_from_module_list(module_list, View.__name__)

        ViewHandler().registerAllViews(view_list, flaskApp)

        test_client = flaskApp.test_client()
        response = test_client.get(View.routes[0])

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_data(), b'hello_view_handler')
        