'''a class is responsible fro scraping a single article'''

from typing import Dict

import bs4

from src.article import Article
from src.request_utils import convert_content_into_soup, get_page_content


class ArticleScraper():
    '''
    base class for article scraper
    has 2 main interfaces:
        * get_page_content: sends http get request to the provided link
        * get_article: returns an Article object
    '''
    link: str
    site: str
    header: Dict
    page_content: str

    def __init__(self, link: str, site: str, header: Dict, **kwargs) -> None:
        self.link = link
        self.site = site
        self.header = header
        self.__dict__.update(kwargs)

    def get_page_content(self) -> None:
        '''updates internal page_content property'''

        self.page_content = get_page_content(self.link, self.header)

    @property
    def get_article(self) -> Article:
        '''transforms internal page content into an Article'''
        if not self.page_content:
            return None

        soup = convert_content_into_soup(self.page_content)

        article_title = self._get_title(soup)
        aricle_text = f'source: {self.link}\n' + self._get_text(soup)
        return Article(
            title=article_title,
            text=aricle_text,
            site=self.site,
        )

    def _get_title(self, element: bs4.element.Tag) -> str:  # pragma: nocover
        return ''

    def _get_text(self, element: bs4.element.Tag) -> str:  # pragma: nocover
        return ''
