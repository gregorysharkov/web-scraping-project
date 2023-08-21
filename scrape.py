'''main module interface'''
from pathlib import Path
from typing import Any, Dict

import yaml

import constants as cn
from src.scraper.eton_scraper import EtonScraper  # type: ignore
from src.scraper.reuters_scraper import ReutersScraper


def scrape_eton(settings: Dict) -> None:
    '''scrape eton.com data'''
    eton_scraper = EtonScraper(
        **settings.get('init_args'),  # type: ignore
        num_articles=settings.get('num_articles'),
    )

    eton_scraper.fetch_content()
    articles = eton_scraper.get_articles()

    for item in articles:
        item.save(cn.OUTPUT_PATH)


def scrape_reuters(settings: Dict) -> None:
    '''scrape reuters.com data'''

    reuters_scraper = ReutersScraper(
        **settings.get('init_args'),  # type: ignore
        num_articles=settings.get('num_articles'),
    )

    reuters_scraper.fetch_content()
    articles = reuters_scraper.get_articles()

    for item in articles:
        item.save(cn.OUTPUT_PATH)


SETTINGS_PATH = Path() / 'conf/scraper_settings.yml'


def load_settings(path: Path) -> Dict[str, Any]:
    '''function loads all settings from the configuration yml'''

    with open(path, 'r') as file:
        settings_dict = yaml.safe_load(file)

    return settings_dict


def load_specific_settings(settings_type: str, path: Path = SETTINGS_PATH) -> Dict[str, Any]:
    '''loads settings specific to the provided settings type'''

    global_settings = load_settings(path)

    assert settings_type in global_settings.get(
        'scraper_itit_settings')  # type: ignore

    init_settings = global_settings.get(
        'scraper_itit_settings').get(settings_type)
    del global_settings['scraper_itit_settings']

    return {
        'init_args': init_settings,
        **global_settings
    }


if __name__ == '__main__':
    scrape_reuters(settings=load_specific_settings('reuters'))
    scrape_eton(settings=load_specific_settings('eton'))
