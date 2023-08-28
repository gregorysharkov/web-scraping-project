'''bqse scraper class'''

from abc import ABC, abstractmethod
from typing import Any, Dict, List

import bs4
from tqdm import tqdm

import src.request_utils as ru
from src.article import Article


class Scraper(ABC):
    '''
    abstract class for object that will extract results from one page
    should have 2 main interfaces:
        * fetch content
        * parse content into a list of articles

    Each inheritent class should redefine:
        * how to get a list of search results (_get_search_results)
        * how to get a link to the article (_get_article_link)
        * which class should be instantiated to parse a single article

    the usage logic is the following:
        1. fetch content
        2. call get_articles, that will:
            a. find search_results in the content
            b. for each result use the appropriate article scraper to create and article
            c. return a list of instantiated articles
    '''
    site_name: str
    base_url: str
    header: Dict[str, Any]
    page_content: str
    search_result_container_name: str
    num_articles: int

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.__dict__.update(kwargs)

    @property
    def _article_scraper(self):  # pragma: nocover
        '''
        property returns an article scraper class that will generate an article
        it should return a class, not an instance
        '''

    # TODO: add dynamic loading
    # solution should be either to use selenium or scrappy + Splash
    # so far for 10 lines the code is complex enough
    def fetch_content(self) -> None:
        '''extracts content from a given page'''

        self.page_content = ru.get_page_content(self.base_url, self.header)

    def get_articles(self) -> List[Article]:
        '''
        function parses the list of articles extracted from the base url
        and returns the list of Article objects
        '''
        raw_articles = self._get_search_results()

        article_list = []
        for raw_article in tqdm(raw_articles[:min(self.num_articles, len(raw_articles))]):
            scraped_article = self._extract_article(raw_article)
            article_list.append(scraped_article)

        return article_list

    def _extract_article(self, element: bs4.element.Tag) -> Article:
        '''extracts article information'''
        link = self._get_article_link(element)

        article_scraper = self._article_scraper(
            link=link,
            site=self.site_name,
            header=self.header,
        )  # type: ignore

        article_scraper.get_page_content()

        return article_scraper.get_article

    @abstractmethod
    def _get_search_results(self) -> List[bs4.element.Tag]:  # pragma: nocover
        '''required to get a list of raw results'''

    @abstractmethod
    def _get_article_link(self, element: bs4.element.Tag) -> str:  # pragma: nocover
        '''required to get a link to the article'''
