from abc import ABC, abstractmethod
from typing import Any, Dict, List, Tuple

import bs4

from article import Article
from request_utils import get_page_content


class Scraper(ABC):
    '''
    abstract class for object that will extract results from one page
    should have 2 main interfaces:
        * fetch content
        * parse content into a list of articles


    Each inheritent class should redefine:
        * how to get a list of search results (_get_search_results)
        * how to get title of each article (_get_title)
        * how to get a link to the article (_get_article_link)
        * how to get a text of the article (_get_article_text using the article link)
    '''
    site_name: str
    base_url: str
    header: Dict[str, Any]
    page_content: str
    search_result_container_name: str

    def __init__(self, **kwargs) -> None:
        super().__init__()
        self.__dict__.update(kwargs)

    # TODO: add dynamic loading
    def fetch_content(self) -> None:
        '''extracts content from a given page'''
        self.page_content = get_page_content(self.base_url, self.header)

    def get_articles(self) -> List[Article]:
        '''
        function parses the list of articles extracted from the base url
        and returns the list of Article objects
        '''
        raw_articles = self._get_search_results()

        article_list = []
        for article in raw_articles:
            article_title, article_content = self._extract_article_information(
                article)
            article_list.append(
                Article(article_title, article_content, self.site_name)
            )

        return article_list

    @abstractmethod
    def _get_search_results(self) -> List[bs4.element.Tag]:
        pass

    def _extract_article_information(self, element: bs4.element.Tag) -> Tuple[str, str]:
        '''extracts article information'''
        title = self._get_title(element)
        link = self._get_article_link(element)
        article_text = self._get_article_text(link)

        return title, article_text

    @abstractmethod
    def _get_title(self, element: bs4.element.Tag) -> str:
        pass

    @abstractmethod
    def _get_article_link(self, element: bs4.element.Tag) -> str:
        pass

    @abstractmethod
    def _get_article_text(self, link: str) -> str:
        pass
