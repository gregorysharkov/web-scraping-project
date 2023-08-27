'''implementation of article scraper for reuters'''

import bs4

from src.parsing_utils import error_on_attribute_error
from src.scraper.article_scraper import ArticleScraper


class ReutersArticleScraper(ArticleScraper):
    '''child class for reuters article scraper'''
    site = 'reuters.com'

    @error_on_attribute_error('Could not parse article title')
    def _get_title(self, element: bs4.element.Tag) -> str:  # pragma: nocover
        '''gets title of the Reuters page'''

        return element\
            .find('h1')\
            .text

    # @error_on_attribute_error('Could not parse article text')
    def _get_text(self, element: bs4.element.Tag) -> str:  # pragma: nocover
        '''gets article text for Reuters page'''

        article_text = element\
            .find_all('div', class_='article-body__content__17Yit')[0]\
            .text
        return article_text
