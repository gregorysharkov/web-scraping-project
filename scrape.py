'''main module interface'''
from typing import Any, Dict

import src.eton_constants as ecn
import src.reuters_constants as rcn
from src.scraper.eton_scraper import EtonScraper  # type: ignore
from src.scraper.reuters_scraper import ReutersScraper


def scrape_eton() -> None:
    '''scrape eton.com data'''
    eton_scraper = EtonScraper(
        **ecn.SCRAPER_INIT_ARGS,
        num_articles=ecn.N_ARTICLES,
    )

    eton_scraper.fetch_content()
    articles = eton_scraper.get_articles()

    for item in articles[:ecn.N_ARTICLES]:
        item.save(ecn.OUTPUT_PATH)


def scrape_reuters() -> None:
    '''scrape reuters.com data'''

    eton_scraper = ReutersScraper(
        **rcn.SCRAPER_INIT_ARGS,
        num_articles=ecn.N_ARTICLES,
    )

    eton_scraper.fetch_content()
    articles = eton_scraper.get_articles()

    for item in articles:
        item.save(rcn.OUTPUT_PATH)


def load_settings(scraper_type: str) -> Dict[str, Any]:
    '''function loads all settings from the configuration yml'''
    # TODO: blueprint of a settings loader function
    pass


if __name__ == '__main__':
    scrape_reuters()
    scrape_eton()
