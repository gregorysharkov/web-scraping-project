'''settings of the reuters scraper'''
from pathlib import Path

SCRAPER_INIT_ARGS = {
    'background_url': 'https://www.reuters.com',
    'search_url': '/tags/mergers-acquisitions/',
    'header': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    },
    'site_name': 'reuters.com',
    'search_result_container_name': 'search-results__item__2oqiX',
}

OUTPUT_PATH = Path().parent / 'scraped_data'
N_ARTICLES = 10
