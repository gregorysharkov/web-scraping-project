'''helper functions to make requests'''

from typing import Dict

import bs4
import requests


def get_page_content(url: str, header: Dict) -> str:
    '''gets content from a page'''

    response = requests.get(url, headers=header)
    return response.content  # type:ignore


def convert_content_into_soup(content: str) -> bs4.BeautifulSoup:
    '''converts given content into soup'''

    return bs4.BeautifulSoup(content, 'html.parser')
