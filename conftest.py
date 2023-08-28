# pylint: disable=C0114, W0613, C0116, C0115
from pathlib import Path

import pytest
import requests

from src.article import Article


@pytest.fixture
def requests_mock(monkeypatch):
    class MockResponse:
        def __init__(self, text):
            self.text = text
            self.content = text.encode('utf-8')

    def mock_get(*args, **kwargs):
        return MockResponse('Mocked response')

    monkeypatch.setattr(requests, 'get', mock_get)


@pytest.fixture
def sample_article():
    return Article(
        title="Sample Article Title",
        text="This is the article text.",
        site="example.com"
    )


@pytest.fixture
def article_with_special_characters():
    return Article(
        title="Special Characters & Article",
        text="Article with special characters.",
        site="example.com"
    )


@pytest.fixture
def temp_folder() -> Path:
    return Path() / 'test' / 'temp_folder'


@pytest.fixture
def mock_get_content():
    def mock_func(url, link):
        return b'Mocked page content'

    return mock_func
