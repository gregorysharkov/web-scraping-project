'''parsing helper functions'''


def error_on_attribute_error(error_string):
    '''
    decorartor that intercepts attribute error when calling a function
    and returns the error string instead
    '''
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except AttributeError:
                return error_string
        return wrapper
    return decorator
