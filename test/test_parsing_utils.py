import pytest

from src.parsing_utils import error_on_attribute_error


def test_error_on_attribute_error():
    error_string = "Custom Error Message"

    @error_on_attribute_error(error_string)
    def test_function(raise_error: bool) -> str:
        if raise_error:
            raise AttributeError(error_string)
        return "Function executed successfully"

    assert test_function(False) == "Function executed successfully"
    assert test_function(True) == error_string
