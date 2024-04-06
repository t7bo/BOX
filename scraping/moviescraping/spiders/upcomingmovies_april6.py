import scrapy


class UpcomingmoviesApril6Spider(scrapy.Spider):
    name = "upcomingmovies_april6"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/calendar/"]

    def parse(self, response):
        pass
