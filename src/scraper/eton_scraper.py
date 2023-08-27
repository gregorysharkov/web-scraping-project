'''scraper used to get and parse eton data'''
from typing import List

import bs4

from src.parsing_utils import error_on_attribute_error
from src.request_utils import convert_content_into_soup
from src.scraper.article_scraper import ArticleScraper
from src.scraper.article_scraper_eton import EtonArticleScraper
from src.scraper.scraper import Scraper


class EtonScraper(Scraper):
    '''implementation of scraping logic for eaton.com'''

    @property
    def _article_scraper(self) -> ArticleScraper:
        return EtonArticleScraper  # type: ignore

    def _get_search_results(self) -> List[bs4.element.Tag]:
        if not self.page_content:
            return None  # type: ignore

        soup = convert_content_into_soup(self.page_content)
        found_items = soup.find_all(
            name='div',
            class_=self.search_result_container_name,
        )

        return found_items

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
