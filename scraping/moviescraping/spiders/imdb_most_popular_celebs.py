import scrapy


class ImdbMostPopularCelebsSpider(scrapy.Spider):
    name = "imdb_most_popular_celebs"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/starmeter/?ref_=nv_cel_m"]

    def parse(self, response):
        pass
