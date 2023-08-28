# pylint: disable=C0114, W0613, C0116, C0115
from bs4 import BeautifulSoup

from src.scraper.article_scraper_eton import EtonArticleScraper
from src.scraper.eton_scraper import EtonScraper


class MockEtonScraper(EtonScraper):
    site_name = 'Mock Site'
    base_url = 'http://mock.com'
    header = {'User-Agent': 'test-user-agent'}
    page_content = '''
        <div class="root responsivegrid">
            <div class="aem-Grid aem-Grid--12 aem-Grid--default--12">
                <div class="responsivegrid aem-GridColumn aem-GridColumn--default--12">
                    Article content goes here.
                </div>
            </div>
        </div>
        '''
    search_result_container_name = 'root'
    num_articles = 5


def test_etonscraper_get_search_results():
    scraper = MockEtonScraper()
    results = scraper._get_search_results()
    assert len(results) == 1
    assert scraper._article_scraper == EtonArticleScraper


def test_etonscraper_get_article_link():
    scraper = MockEtonScraper()
    element = BeautifulSoup(
        '<h4 class="results-list-submodule__name b-heading-h5"><a class="results-list-submodule__name-link" href="http://mock.com/article">Link</a></h4>', 'html.parser')
    link = scraper._get_article_link(element)
    assert link == 'http://mock.com/article'
