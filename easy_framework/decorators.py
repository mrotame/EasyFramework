from easy_framework._context import cache

def register_api_exception(cls: BaseException):
    if 'api_exception_list' not in cache or not isinstance(cache['api_exception_list'].get_value(), list):
        cache['api_exception_list'] = []

    cache['api_exception_list'].append(cls)

    return cls