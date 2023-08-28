# pylint: disable=C0114, W0613, C0116, C0115
import bs4

from src.scraper.article_scraper_reuters import ReutersArticleScraper
from src.scraper.reuters_scraper import ReutersScraper


class MockReutersScraper(ReutersScraper):
    site_name = 'Mock Site'
    # base_url = 'http://mock.com'
    header = {'User-Agent': 'test-user-agent'}
    page_content = '''
        <ul>
            <li class="search_result">
                <div data-testid="MediaStoryCard">
                    <div>
                        <h3>
                            <a href='/media_article_id'>some text</a>
                        </h3>
                    </div>
                </div>
            </li>
            <li class="search_result">
                <div data-testid="TextStoryCard">
                    <a href="/something_else">a</a>
                    <a href="/text_article_id">b</a>
                </div>
            </li>
            <li class="search_result">
                <div data-testid="something else">
                    <a href="/something_else">a</a>
                    <a href="/text_article_id">b</a>
                </div>
            </li>
        </ul>
        '''
    search_result_container_name = 'search_result'
    num_articles = 5
    background_url = 'http://mock.com'
    search_url = '/articles/'


def test_reuters_scraper_get_search_results():
    scraper = MockReutersScraper()
    assert scraper._article_scraper == ReutersArticleScraper
    assert scraper.base_url == 'http://mock.com/articles/'
    assert scraper._get_article_url(
        '/article_id') == 'http://mock.com/article_id'
    results = scraper._get_search_results()
    assert len(results) == 3


def test_reuters_scraper_get_article_link():
    scraper = MockReutersScraper()
    results = scraper._get_search_results()
    article_urls = []
    for result in results:
        article_urls.append(scraper._get_article_link(result))

    assert 'http://mock.com/media_article_id' in article_urls
    assert 'http://mock.com/text_article_id' in article_urls
