# pylint: disable=C0114, W0613, C0116, C0115
import bs4
import pytest
import requests

from src.request_utils import convert_content_into_soup, get_page_content


def test_get_page_content(requests_mock):
    header = {'User-Agent': 'test-user-agent'}
    content = get_page_content('http://example.com', header)
    assert content == b'Mocked response'


def test_get_page_content_with_invalid_url():
    header = {'User-Agent': 'test-user-agent'}
    with pytest.raises(requests.RequestException):
        get_page_content('invalid-url', header)


def test_valid_html():
    content = '<html><head><title>Test Page</title></head><body><p>Hello, world!</p></body></html>'
    soup = convert_content_into_soup(content)
    assert isinstance(soup, bs4.BeautifulSoup)
    assert soup.title.string == 'Test Page'
    assert soup.find('p').string == 'Hello, world!'
