# pylint: disable=C0114, W0613, C0116, C0115
import pytest
import requests

from src.request_utils import get_page_content


def test_get_page_content(requests_mock):
    header = {'User-Agent': 'test-user-agent'}
    content = get_page_content('http://example.com', header)
    assert content == b'Mocked response'


def test_get_page_content_with_invalid_url():
    header = {'User-Agent': 'test-user-agent'}
    with pytest.raises(requests.RequestException):
        get_page_content('invalid-url', header)
