# pylint: disable=C0114, W0613, C0116, C0115
from pathlib import Path
from unittest.mock import MagicMock, patch

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
def mock_get_page_content(monkeypatch):
    # Mocking get_page_content using monkeypatch
    def mock_get_content(url, header):
        return b'Mocked page content'

    monkeypatch.setattr("src.get_page_content", mock_get_content)


@pytest.fixture
def mock_eton_get_page_content(monkeypatch):
    def eaton_mock_get_content(url, header):
        # Mock article page content
        article_page_content = '''
        <div class="root responsivegrid">
            <div class="aem-Grid aem-Grid--12 aem-Grid--default--12">
                <div class="responsivegrid aem-GridColumn aem-GridColumn--default--12">
                    Article content goes here.
                </div>
            </div>
        </div>
        '''
        return article_page_content.encode('utf-8')

    monkeypatch.setattr(
        "src.get_page_content", eaton_mock_get_content)
