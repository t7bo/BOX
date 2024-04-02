from typing import Iterable
import scrapy
import pandas as pd
from fake_useragent import UserAgent
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from ..middlewares import RandomUserAgentMiddleware
import time
from ..items import MovieItem

class ImdbMoviesSpider(scrapy.Spider):
    name = "imdb_movies"
    allowed_domains = ["www.imdb.com"]
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'moviescraping.middlewares.CustomMiddleware': 400,
        },
        'ITEM_PIPELINES' : {
            "moviescraping.pipelines.MoviesPipeline": 300
        }
    }
    
    def start_requests(self):
    
        data = pd.read_csv(r'C:\Users\Thibaut\Documents\SIMPLON\DEV-IA\BOXOFFICE\scraping\data\imdb_movies_id.csv')
        for value in data.movie_id:
            url = f"https://www.imdb.com/title/{value}"
            # headers = {'User-Agent': get_random_user_agent()}
            yield scrapy.Request(url=url, callback=self.parse)
        

    def parse(self, response):
        
        try:        
            movie = MovieItem()
            movie['movie_url'] = response.url
            movie['movie_id'] = 'tt' + str(''.join(filter(str.isdigit, response.url)))
            movie['year'] = response.xpath('//main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/ul/li[1]/a/text()').get()
            movie['movie_title'] = response.xpath('//h1[@data-testid="hero__pageTitle"]/span[@data-testid="hero__primary-text"]/text()').get()
            movie['movie_original_title'] = response.xpath('//h1[@data-testid="hero__pageTitle"]/following-sibling::div/text()').get()
            movie['movie_length'] = response.css('li[role="presentation"]::text').get()
            movie['movie_imdb_rating'] = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span/text()').get()
            movie['movie_imdb_nb_of_ratings'] = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]//following-sibling::div/text()').get()
            movie['movie_imdb_popularity'] = response.xpath('//div[@data-testid="hero-rating-bar__popularity__score"]/text()').get()
            movie['movie_synopsis'] = response.xpath('//span[@data-testid="plot-l"]/text()').get()
            movie['movie_director'] = response.xpath('//section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li/a/text()').getall()
            movie['movie_cast'] = response.xpath('//a[@data-testid="title-cast-item__actor"]/text()').getall()
            movie['movie_categories'] = response.xpath('//div[@class="ipc-chip-list__scroller"]/a/span[@class="ipc-chip__text"]/text()').getall()
            movie['movie_imdb_metascore'] = response.css('span.metacritic-score-box::text').get()
            movie['movie_countries'] = response.xpath('//li[@data-testid="title-details-origin"]/div/ul/li/a/text()').getall()
            movie['movie_production_companies'] = response.xpath('//li[@data-testid="title-details-companies"]/div/ul/li/a/text()').getall()
            movie['movie_budget'] = response.xpath('//li[@data-testid="title-boxoffice-budget"]/div/ul/li/span/text()').get()
            movie['movie_us_boxoffice'] = response.xpath('//li[@data-testid="title-boxoffice-grossdomestic"]/div/ul/li/span/text()').get()
            movie['movie_boxoffice'] = response.xpath('//li[@data-testid="title-boxoffice-cumulativeworldwidegross"]/div/ul/li/span/text()').get()
            yield movie
        except scrapy.exceptions.IgnoreRequest:  # Si erreur 503 est levée
                    self.logger.warning("Erreur 503 détectée. Mise en pause du scraping pendant 120 secondes.")
                    time.sleep(180)  # Mettre en pause pendant 3min
                    yield scrapy.Request(response.url, callback=self.parse)  # Reprendre le scraping après la pause
