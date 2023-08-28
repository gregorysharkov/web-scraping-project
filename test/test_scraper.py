# pylint: disable=C0114, W0613, C0116, C0115
from typing import Dict

import bs4

from src.article import Article
from src.scraper.article_scraper import ArticleScraper
from src.scraper.scraper import Scraper


class MockArticleScraper(ArticleScraper):
    page_content = ''

    @property
    def get_article(self):
        return Article('title', 'text', 'site')

    def get_page_content(self):
        self.page_content = ''


class MockScraper(Scraper):
    site_name = 'Mock Site'
    base_url = 'http://mock.com'
    header = {'User-Agent': 'test-user-agent'}
    num_articles = 5

    @property
    def _article_scraper(self):
        return MockArticleScraper

    def _get_search_results(self):
        return [bs4.BeautifulSoup(f'<div class="article-{i}">Article {i}</div>', 'html.parser')
                for i in range(1, 6)]

    def _get_article_link(self, element):
        return f'http://mock.com/article/{element.get_text()}'


def test_fetch_content(monkeypatch, mock_get_content):

    monkeypatch.setattr("src.request_utils.get_page_content",
                        mock_get_content)
    scraper = MockScraper()
    scraper.fetch_content()
    assert scraper.page_content == b'Mocked page content'


def test_get_articles():
    class MockScraperExtractArticle(MockScraper):
        def _extract_article(self, element: bs4.element.Tag) -> Article:
            return Article('article', 'text', 'site')

    scraper = MockScraperExtractArticle()
    article_list = scraper.get_articles()
    assert len(article_list) == scraper.num_articles


def test_extract_arcticle():
    scraper = MockScraper()
    article = scraper._extract_article(
        bs4.BeautifulSoup('<div>something</div>', features="html.parser")
    )
    assert article.title == 'title'
