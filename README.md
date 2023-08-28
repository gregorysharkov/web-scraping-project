# web-scraping-project

## Problem description
### Objective:
The task is to extract articles from two distinct websites, retrieving 10 articles from each link. The extracted data should be saved in a local file.

### Problem Description:
1. Websites to Scrape:
* Eaton: Eaton News Releases (https://www.eaton.com/us/en-us/company/news-insights/news-releases.html)
* Reuters: Reuters Mergers & Acquisitions (https://www.reuters.com/tags/mergers-acquisitions/)

2. Data Points to Extract:
* Article Title
* Article Link
* Full Article Text

3. Output:
* Save the extracted data in individual local files, using the article title as the file name.

## Solution
My goal was to develop a script that would scrape both sources using `BeautifulSoup` python library. This is my promary choice when it comes to vanila web scraping. Both web sites allow getting the first ten results using a static web request.

Base element of the system is an `Article`. It is a data class that contains 3 reaquired elements:
* Title
* Link
* Full text

This class is responsible for storing the article content in a provided location using `save` method

The next element of the system is a `scraper`. Scraper is responsible for retrieving invformation from a web site and for parsing information from a given location.

Scraper is an abstract class that has 2 public interfaces:
* fetch content from the web site – returns content of the list of results
* get_articles — generates a list of `article` objects from the the page content

2 child classes that inherit from `scraper` are `EtonScraper` and `ReutersScraper`.

This setup alows further extention by adding new scrapers in future as well a possibility to address the problem of dynamic content in future by overriding the fetch method (using `selenium` package for example).

The `get_articles` method iterates over search results and instantiates `Articles` using `ArticleScrapers`. Each ArticleScraper is responsible for fetching results from a URL provided by `scraper` class and alows
1. get the title
2. get the article content using the article url

All scraper settings are located in `/conf/` folder in a separate yml file


## Setup and execution
1. Clone repository
2. Install dependencies
```bash
git clone https://github.com/gregorysharkov/web-scraping-project.git
pip install -r requirements.txt
```
The main script is located in `scrape.py`, all output files are stored in the `scraped_data` folder.
```bash
python scrape.py
```

## Further improvements
* ~~add unit tests~~
* address dynamic content feature
* add support for parallel processing