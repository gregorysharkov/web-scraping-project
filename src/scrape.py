'''main module interface'''

from tqdm import tqdm

import eton_constants as ecn
import reuters_constants as rcn
from scraper.eton_scraper import EtonScraper
from scraper.reuters_scraper import ReutersScraper


def scrape_eton() -> None:
    '''scrape eton.com data'''
    eton_scraper = EtonScraper(
        site_name=ecn.WEBSITE_NAME,
        base_url=ecn.BASE_URL,
        header=ecn.HEADER,
        search_result_container_name=ecn.CONTAINER_CLASS_NAME,
    )

    eton_scraper.fetch_content()
    articles = eton_scraper.get_articles()

    for item in articles[:ecn.N_ARTICLES]:
        item.save(ecn.OUTPUT_PATH)


def scrape_reuters() -> None:
    '''scrape reuters.com data'''

    eton_scraper = ReutersScraper(
        **rcn.SCRAPER_INIT_ARGS,
    )

    eton_scraper.fetch_content()
    articles = eton_scraper.get_articles()

    for item in tqdm(articles[:rcn.N_ARTICLES]):
        item.save(rcn.OUTPUT_PATH)


if __name__ == '__main__':
    scrape_reuters()
