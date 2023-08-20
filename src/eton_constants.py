from pathlib import Path

BASE_URL = 'https://www.eaton.com/us/en-us/company/news-insights/news-releases.html'
HEADER = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0'
}
CONTAINER_CLASS_NAME = 'results-list-submodule results-list-submodule--type-news-and-insights'
WEBSITE_NAME = 'eaton.com'
OUTPUT_PATH = Path().parent / 'scraped_data'

N_ARTICLES = 10
