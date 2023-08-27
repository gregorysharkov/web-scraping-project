'''implementation of article scraper for eaton'''

import bs4

from src.parsing_utils import error_on_attribute_error
from src.scraper.article_scraper import ArticleScraper


class EtonArticleScraper(ArticleScraper):
    '''child class for eaton article scraper'''
    site = 'eton.com'

    @error_on_attribute_error('Could not parse article title')
    def _get_title(self, element: bs4.element.Tag) -> str:  # pragma: nocover
        '''gets title of an Eaton page'''
        title = element\
            .find_all('div', class_='eaton-title')

        if not title:
            raise AttributeError()

        article_title = title[0].text.strip()  # type: ignore
        return article_title

    @error_on_attribute_error('Could not parse article text')
    def _get_text(self, element: bs4.element.Tag) -> str:  # pragma: nocover
        '''gets text of the article'''
        article_text = element\
            .find('div', class_='root responsivegrid')\
            .find('div', class_='aem-Grid aem-Grid--12 aem-Grid--default--12')\
            .find(
                name='div',
                class_='responsivegrid aem-GridColumn aem-GridColumn--default--12'
            )\
            .text
        return article_text
