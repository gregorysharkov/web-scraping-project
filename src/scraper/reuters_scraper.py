'''scraper used to get and parse reuters data'''
from typing import List

import bs4

from src.parsing_utils import error_on_attribute_error
from src.request_utils import get_page_content

from .scraper import Scraper


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

    def _get_article_url(self, href: str) -> str:
        return self.background_url + href

    def _get_search_results(self) -> List[bs4.element.Tag]:
        if not self.page_content:
            return None  # type: ignore

        soup = bs4.BeautifulSoup(self.page_content, 'html.parser')
        found_items = soup.find_all(
            name='li',
            class_=self.search_result_container_name,
        )

        return found_items

    @error_on_attribute_error('Could not parse article title')
    def _get_title(self, element: bs4.element.Tag) -> str:
        '''gets title text from a given element'''

        item_container = element.find('div')  # type: Tag
        item_type = item_container.get('data-testid')  # type: ignore

        if item_type == 'MediaStoryCard':
            return item_container\
                .find('div')\
                .find('h3')\
                .text  # type: ignore

        elif item_type == 'TextStoryCard':
            return item_container\
                .find_all('a')[1]\
                .text

        raise AttributeError()

    @error_on_attribute_error('Could not parse article link')
    def _get_article_link(self, element: bs4.element.Tag) -> str:
        '''gets article url from a given element'''

        item_container = element.find('div')  # type: Tag
        item_type = item_container.get('data-testid')

        if item_type == 'MediaStoryCard':
            return item_container\
                .find('div')\
                .find('h3')\
                .find('a')\
                .get('href')  # type: ignore

        elif item_type == 'TextStoryCard':
            return item_container\
                .find_all('a')[1]\
                .get('href')  # type: ignore

        raise AttributeError()

    @error_on_attribute_error('Could not parse article title')
    def _get_article_text(self, link: str) -> str:
        '''function gets text from an article'''

        article_url = self._get_article_url(link)
        article_page = get_page_content(article_url, self.header)
        soup = bs4.BeautifulSoup(article_page, 'html.parser')

        article_content = soup\
            .find_all('div', class_='article__content__6hMn9')

        if not article_content:
            raise AttributeError()

        return f'source: {link}\n' + article_content[0].text  # type: ignore
