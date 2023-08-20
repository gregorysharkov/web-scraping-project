'''eton scraper contants'''

from pathlib import Path

SCRAPER_INIT_ARGS = {
    'base_url': 'https://www.eaton.com/us/en-us/company/news-insights/news-releases.html',
    'header': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
    },
    'site_name': 'eaton.com',
    'search_result_container_name': 'results-list-submodule results-list-submodule--type-news-and-insights',
}

OUTPUT_PATH = Path() / 'scraped_data'
N_ARTICLES = 10
