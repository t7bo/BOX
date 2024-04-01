import scrapy


class ImdbMoviesSpider(scrapy.Spider):
    name = "imdb_movies"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/search/title/?title_type=feature"]

    def parse(self, response):
        pass
