'''helper functions to make requests'''

from typing import Dict

import requests


def get_page_content(url: str, header: Dict) -> str:
    '''gets content from a page'''

    response = requests.get(url, headers=header)
    return response.content
