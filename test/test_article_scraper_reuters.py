from src.scraper.article_scraper_reuters import ReutersArticleScraper


class MockReutersScraper(ReutersArticleScraper):
    def get_page_content(self) -> None:
        self.page_content = '''
            <!DOCTYPE html>
            <html>
            <head>
                <title>Test Page</title>
            </head>
            <body>
                <h1>Article Title</h1>
                <div class="article-body__content__17Yit">This is a test article.</p>
            </body>
            </html>
        '''


def test_reuters_scraper():
    scraper = MockReutersScraper(
        link="some_link",
        site="example.com",
        header={"User-Agent": "Mozilla/5.0"},
    )  # type: ignore

    scraper.get_page_content()

    article = scraper.get_article

    assert article.title == 'Article Title'
    assert article.text == 'source: some_link\nThis is a test article.\n'
