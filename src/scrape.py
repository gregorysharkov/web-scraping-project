from typing import Dict, List, Tuple

import bs4

import constants as cn
from article import Article
from request_utils import get_page_content


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

    title = get_title(element)
    link = get_article_link(element)
    article_text = get_article_text(link, cn.HEADER)

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


if __name__ == '__main__':

    page_content = get_page_content(cn.BASE_URL, header=cn.HEADER)
    articles = get_search_results(page_content, cn.CONTAINER_CLASS_NAME)
    extracted_articles = []
    for item in articles[:2]:
        article = Article(*extract_article_information(item), cn.WEBSITE_NAME)
        extracted_articles.append(article)
        article.save(cn.OUTPUT_PATH)
