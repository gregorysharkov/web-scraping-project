from pathlib import Path
from typing import Dict, List, Tuple

import bs4 as bs4
import requests

BASE_URL = 'https://www.eaton.com/us/en-us/company/news-insights/news-releases.html'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
}
CONTAINER_CLASS_NAME = 'results-list-submodule results-list-submodule--type-news-and-insights'
WEBSITE_NAME = 'eaton.com'
OUTPUT_PATH = Path().parent / 'scraped_data'


def error_on_attribute_error(error_string):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                return result
            except AttributeError:
                return error_string
        return wrapper
    return decorator


def get_page_content(url: str, header: Dict) -> str:
    '''gets content from a page'''

    response = requests.get(url, headers=header)
    return response.content


def get_search_results(content: str, container_class_name: str) -> List[str]:
    '''get list of search results given the content'''

    if not content:
        return None

    soup = bs4.BeautifulSoup(content, 'html.parser')
    found_items = soup.find_all(
        name='div',
        class_=container_class_name,
    )

    return found_items


def extract_article_information(element: bs4.element.Tag) -> Tuple[str, str]:
    '''
    extracts name, link and the content of a single article

    Args:
        element: an element to be parsed

    Returns:
        tuple containing title, link and the article text
    '''

    title = f'{WEBSITE_NAME} - {get_title(element)}'
    link = get_article_link(element)
    article_text = get_article_text(link, HEADER)

    return title, article_text


@error_on_attribute_error('Could not parse article title')
def get_title(element: bs4.element.Tag) -> str:
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
def get_article_link(element: bs4.element.Tag) -> str:
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


@error_on_attribute_error('Could not parse article text')
def get_article_text(link: str, header: Dict) -> str:
    '''function gets text from an article'''

    article_page = get_page_content(link, header)
    soup = bs4.BeautifulSoup(article_page, 'html.parser')

    article_content = soup\
        .find('div', class_='root responsivegrid')\
        .find('div', class_='aem-Grid aem-Grid--12 aem-Grid--default--12')\
        .find(
            name='div',
            class_='responsivegrid aem-GridColumn aem-GridColumn--default--12'
        )

    return f'source: {link}' + article_content.text


def save_article(article_name: str, article_text: str, output_path: Path = OUTPUT_PATH) -> None:
    '''saves given article in the given path'''

    file_name = output_path / f'{article_name}.txt'
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(article_text)


if __name__ == '__main__':

    page_content = get_page_content(BASE_URL, header=HEADER)
    articles = get_search_results(page_content, CONTAINER_CLASS_NAME)
    extracted_articles = []
    for item in articles[:2]:
        save_article(*extract_article_information(item))

    # print(extracted_articles)
