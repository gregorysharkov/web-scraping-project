'''scraper used to get and parse eton data'''
from typing import List

import bs4

from src.parsing_utils import error_on_attribute_error
from src.request_utils import get_page_content
from src.scraper.scraper import Scraper


class EtonScraper(Scraper):
    '''implementation of scraping logic for eaton.com'''

    def _get_search_results(self) -> List[bs4.element.Tag]:
        if not self.page_content:
            return None  # type: ignore

        soup = bs4.BeautifulSoup(self.page_content, 'html.parser')
        found_items = soup.find_all(
            name='div',
            class_=self.search_result_container_name,
        )

        return found_items

    @error_on_attribute_error('Could not parse article title')
    def _get_title(self, element: bs4.element.Tag) -> str:
        '''gets title text from a given element'''

        return element\
            .find(
                name='h4',
                class_='results-list-submodule__name b-heading-h5'
            )\
            .find(
                'a',
                class_='results-list-submodule__name-link'
            )\
            .find(
                name='span',
                class_='name-label',
            )\
            .text  # type: ignore

    @error_on_attribute_error('Could not parse article link')
    def _get_article_link(self, element: bs4.element.Tag) -> str:
        '''gets article url from a given element'''

        return element\
            .find(
                name='h4',
                class_='results-list-submodule__name b-heading-h5',
            )\
            .find(
                name='a',
                class_='results-list-submodule__name-link',
            )\
            .get('href')  # type: ignore

    @error_on_attribute_error('Could not parse article title')
    def _get_article_text(self, link: str) -> str:
        '''function gets text from an article'''

        article_page = get_page_content(link, self.header)
        soup = bs4.BeautifulSoup(article_page, 'html.parser')

        article_content = soup\
            .find('div', class_='root responsivegrid')\
            .find('div', class_='aem-Grid aem-Grid--12 aem-Grid--default--12')\
            .find(
                name='div',
                class_='responsivegrid aem-GridColumn aem-GridColumn--default--12'
            )

        return f'source: {link}\n' + article_content.text
