import scrapy

class ImdbMostPopularCelebsSpider(scrapy.Spider):
    name = "imdb_most_popular_celebs"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/chart/starmeter/?ref_=nv_cel_m"]

    # custom_settings = {

    #     'ITEM_PIPELINES' : {
    #         "moviescraping.pipelines.MoviesPipeline": 300
    #     }
    # }

    def parse(self, response):

        yield {
            'celebrity' : response.xpath('//div[@data-testid="nlib-title"]/a/h3/text()').getall()
        }
