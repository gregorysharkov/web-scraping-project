from bs4 import BeautifulSoup
from pytest import MonkeyPatch

from src.request_utils import convert_content_into_soup
from src.scraper.eton_scraper import EtonScraper


class MockEtonScraper(EtonScraper):
    site_name = 'Mock Site'
    base_url = 'http://mock.com'
    header = {'User-Agent': 'test-user-agent'}
    page_content = ''
    search_result_container_name = 'results'
    num_articles = 5

    def _get_search_results(self):
        return [
            BeautifulSoup(
                f'<div class="article-{i}">Article {i}</div>', 'html.parser'
            ) for i in range(1, 6)
        ]


def test_etonscraper_get_search_results():
    scraper = MockEtonScraper()
    scraper.page_content = '<div class="results">Mock content</div>'
    results = scraper._get_search_results()
    assert len(results) == 5


def test_etonscraper_get_title():
    scraper = MockEtonScraper()
    element = BeautifulSoup(
        '<h4 class="results-list-submodule__name b-heading-h5"><a class="results-list-submodule__name-link"><span class="name-label">Title</span></a></h4>', 'html.parser')
    title = scraper._get_title(element)
    assert title == 'Title'


def test_etonscraper_get_article_link():
    scraper = MockEtonScraper()
    element = BeautifulSoup(
        '<h4 class="results-list-submodule__name b-heading-h5"><a class="results-list-submodule__name-link" href="http://mock.com/article">Link</a></h4>', 'html.parser')
    link = scraper._get_article_link(element)
    assert link == 'http://mock.com/article'

# Too complicated, I cannot override the get_page_content method inside the _get_article_text
# TODO: add dependency injection here
# def test_etonscraper_get_article_text(mock_eton_get_page_content):
#     scraper = MockEtonScraper()
#     article_text = scraper._get_article_text('http://mock.com/article')
#     assert 'source: http://mock.com/article' in article_text
#     assert 'Mocked page content' in article_text


def test_eton_scraper_get_article_text(mock_article_content: str):
    class MockArticleEtonScraper(MockEtonScraper):
        def _get_article_content(self, link) -> BeautifulSoup:
            return convert_content_into_soup(mock_article_content)

    scraper = MockArticleEtonScraper()
    article_text = scraper._get_article_text('http://mock.com/article')
    assert 'source: http://mock.com/article' in article_text
    assert 'Mocked page content' in article_text


def test_eton_scraper_get_article_content(monkeypatch: MonkeyPatch, mock_article_content: str):
    monkeypatch.setattr('src.request_utils.get_page_content',
                        lambda url, header: mock_article_content)
    from src.scraper.eton_scraper import EtonScraper

    scraper = EtonScraper(header={})
    article_soup = scraper._get_article_content('https://some_link')
    print(repr(article_soup))
