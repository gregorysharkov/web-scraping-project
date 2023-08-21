from unittest.mock import MagicMock, patch

import pytest
from bs4 import BeautifulSoup

from src.article import Article
from src.scraper.scraper import Scraper


class MockScraper(Scraper):
    site_name = 'Mock Site'
    base_url = 'http://mock.com'
    header = {'User-Agent': 'test-user-agent'}
    page_content = ''
    search_result_container_name = 'results'
    num_articles = 5

    def _get_search_results(self):
        return [BeautifulSoup(f'<div class="article-{i}">Article {i}</div>', 'html.parser')
                for i in range(1, 6)]

    def _get_title(self, element):
        return element.get_text()

    def _get_article_link(self, element):
        return f'http://mock.com/article/{element.get_text()}'

    def _get_article_text(self, link):
        return f'This is the content of {link}'


def test_extract_article_information():
    scraper = MockScraper()
    element = BeautifulSoup(
        '<div class="article-1">Article 1</div>', 'html.parser')
    title, article_text = scraper._extract_article_information(element)
    expected_link = 'http://mock.com/article/Article 1'
    assert title == 'Article 1'
    assert article_text == f'This is the content of {expected_link}'


def test_get_articles():
    scraper = MockScraper()
    article_list = scraper.get_articles()
    assert len(article_list) == 5
    assert isinstance(article_list[0], Article)
    assert article_list[0].title == 'Article 1'
    assert article_list[0].text == 'This is the content of http://mock.com/article/Article 1'
    assert article_list[0].site == 'Mock Site'
