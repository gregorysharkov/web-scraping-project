'''scraper used to get and parse reuters data'''
from typing import List

import bs4

from src.parsing_utils import error_on_attribute_error
from src.request_utils import convert_content_into_soup
from src.scraper.article_scraper import ArticleScraper
from src.scraper.article_scraper_reuters import ReutersArticleScraper
from src.scraper.scraper import Scraper


class ReutersScraper(Scraper):
    '''
    class is responsible for fetching reuters data
    '''
    background_url: str
    search_url: str

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    @property
    def base_url(self) -> str:
        '''constructs base url from background and search urls'''
        return self.background_url + self.search_url

    @property
    def _article_scraper(self) -> ArticleScraper:
        return ReutersArticleScraper  # type: ignore

    def _get_article_url(self, href: str) -> str:
        '''
        retuters provides only partial url in the links
        so we need to concatenate them inside with the base url
        '''
        return self.background_url + href

    def _get_search_results(self) -> List[bs4.element.Tag]:
        '''returns a list of bs elements containing found articles'''
        if not self.page_content:
            return None  # type: ignore

        soup = convert_content_into_soup(self.page_content)
        found_items = soup.find_all(
            name='li',
            class_=self.search_result_container_name,
        )

        return found_items

    @error_on_attribute_error('Could not parse article link')
    def _get_article_link(self, element: bs4.element.Tag) -> str:
        '''gets article url from a given element'''

        item_container = element.find('div')  # type: Tag
        item_type = item_container.get('data-testid')

        if item_type == 'MediaStoryCard':
            element_link = item_container\
                .find('div')\
                .find('h3')\
                .find('a')\
                .get('href')  # type: ignore
            return self._get_article_url(element_link)

        elif item_type == 'TextStoryCard':
            element_link = item_container\
                .find_all('a')[1]\
                .get('href')  # type: ignore

            return self._get_article_url(element_link)

        raise AttributeError()
