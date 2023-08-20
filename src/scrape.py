import constants as cn
from scraper.eton_scraper import EtonScraper

if __name__ == '__main__':

    scraper = EtonScraper(
        site_name=cn.WEBSITE_NAME,
        base_url=cn.BASE_URL,
        header=cn.HEADER,
        search_result_container_name=cn.CONTAINER_CLASS_NAME,
    )

    scraper.fetch_content()
    articles = scraper.get_articles()

    for item in articles[:cn.N_ARTICLES]:
        item.save(cn.OUTPUT_PATH)
