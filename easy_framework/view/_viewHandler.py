import typing as t
import glob
import os
from flask import Flask
from flask.views import MethodView
from pathlib import Path
import importlib
from loguru import logger
from easy_framework._context import cache

class ViewHandler:
    
    @classmethod
    def register_views(cls, directory: str|Path, flaskApp: Flask, view_class_name: str):
        '''
        Import and register all views in a directory
        '''
        module_list = cls.get_modules(cls, directory)
        view_list = cls.filter_views_from_module_list(cls, module_list, view_class_name)
        cls.registerAllViews(cls, view_list, flaskApp)

    def get_modules(self, directory:str|Path):
        '''
        get modules from directory using the FilterModules class
        '''
        if not os.path.isabs(directory):
            directory = cache.root_dir.joinpath(directory)
            
        return FilterModules().getModules(directory)
    
    def filter_views_from_module_list(self, module_list:t.List[str], view_class_name:str)-> t.List[MethodView]:
        '''
        returns a list of modules that contains the View class
        '''

        view_list = []
        for module in module_list:
            module = importlib.import_module(module, module)

            if hasattr(module, view_class_name):
                view = getattr(module, view_class_name)
                if view not in view_list:
                    view_list.append(view)
        return view_list

    def registerAllViews(self, view_list: t.List[MethodView], flaskApp:Flask):
        '''
        Register all the views in the flask app
        '''

        logger.info("Adding url rules...")
        for view in view_list:

            for route in view.routes:
                view_id = view.__name__+'.'+ route
                flaskApp.add_url_rule(route, view_id, view.as_view(view_id))

        logger.info(f"{len(view_list)} urls registered")

class FilterModules:
    '''
    Access a specific directory, get all python files
    and convert from file path to module format
    '''
    def getModules(self, directory:str|Path)->t.List[str]:
        all_files = self.find_all_python_files(directory)
        view_list = self.remove_init_from_file_list(all_files)
        module_list = self.convert_from_path_to_module(view_list)
        return module_list
    
    def find_all_python_files(self, directory:str|Path)-> t.List[str|Path]:
        '''
        Find python files in a directory
        '''
        glob_iterator = glob.iglob(str(directory) + '/**/*.py', recursive=True)
        return [i for i in glob_iterator if os.path.isfile(i)]
    
    def remove_init_from_file_list(self, python_file_list:t.List[str|Path])-> t.List[str|Path]:
        '''
        Remove the __init__.py file from the files list
        '''
        return [i for i in python_file_list if "__init__.py" not in i]
    
    def convert_from_path_to_module(self, view_list:t.List[str|Path])-> t.List[str]:
        '''
        Convert from file path to module path
        '''
        return [i.replace(os.getcwd(),'')[:-3].replace('/','.').strip('.') for i in view_list]