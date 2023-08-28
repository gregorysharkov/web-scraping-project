from unittest.mock import Mock, patch

import pytest
from bs4 import BeautifulSoup

from src.scraper.article_scraper import ArticleScraper


# Mocking the get_page_content and convert_content_into_soup functions
@pytest.fixture
def mock_get_page_content(monkeypatch):
    def mock_get(*args, **kwargs):
        return "Mocked Page Content"
    monkeypatch.setattr(
        "src.scraper.article_scraper.get_page_content", mock_get)


def test_article_scraper_constructor():
    scraper = ArticleScraper(
        link='some_link',
        site='some_site',
        header={'some_key': 'some_value'},
        new_arg='some_new_value',
        page_content='something'
    )
    assert scraper.link == 'some_link'
    assert scraper.site == 'some_site'
    assert scraper.header.get('some_key') == 'some_value'
    assert scraper.new_arg == 'some_new_value'


def test_get_article(mock_get_page_content):
    link = "http://example.com"
    site = "Example Site"
    header = {"User-Agent": "Mozilla/5.0"}
    scraper = ArticleScraper(link, site, header)
    scraper.get_page_content()

    article = scraper.get_article

    assert article.title == ""
    assert article.text == "source: http://example.com\n"
    assert article.site == "Example Site"


def test_empty_article():
    link = "http://example.com"
    site = "Example Site"
    header = {"User-Agent": "Mozilla/5.0"}
    page_content = None
    scraper = ArticleScraper(link, site, header, page_content=page_content)

    article = scraper.get_article
    assert article is None
