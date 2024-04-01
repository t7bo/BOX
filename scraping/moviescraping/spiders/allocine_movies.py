import scrapy


class AllocineMoviesSpider(scrapy.Spider):
    name = "allocine_movies"
    allowed_domains = ["www.allocine.fr"]
    start_urls = ["https://www.allocine.fr/films/decennie-2020"]

    def parse(self, response):
        pass
