# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviescrapingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ImdbOscarPageItem(scrapy.Item):
    url = scrapy.Field()
    year = scrapy.Field()
    categories = scrapy.Field()
    winners = scrapy.Field()
    
class MovieItem(scrapy.Item):
    movie_id = scrapy.Field()
    movie_url = scrapy.Field()
    year = scrapy.Field()
    release_date = scrapy.Field()
    movie_title = scrapy.Field()
    movie_original_title = scrapy.Field()
    movie_length = scrapy.Field()
    movie_imdb_rating = scrapy.Field()
    movie_imdb_nb_of_ratings = scrapy.Field()
    movie_imdb_popularity = scrapy.Field()
    movie_synopsis = scrapy.Field()
    movie_director = scrapy.Field()
    movie_cast = scrapy.Field()
    movie_categories = scrapy.Field()
    movie_imdb_metascore = scrapy.Field()
    movie_countries = scrapy.Field()
    movie_production_companies = scrapy.Field()
    movie_budget = scrapy.Field()
    movie_us_boxoffice = scrapy.Field()
    movie_boxoffice = scrapy.Field()
    movie_poster = scrapy.Field()
    
class UpcomingMovieItem(scrapy.Item):
    movie_id = scrapy.Field()
    movie_url = scrapy.Field()
    release_date = scrapy.Field()
    movie_title = scrapy.Field()
    movie_original_title = scrapy.Field()
    movie_length = scrapy.Field()
    movie_imdb_rating = scrapy.Field()
    movie_imdb_nb_of_ratings = scrapy.Field()
    movie_imdb_popularity = scrapy.Field()
    movie_synopsis = scrapy.Field()
    movie_director = scrapy.Field()
    movie_cast = scrapy.Field()
    movie_categories = scrapy.Field()
    movie_imdb_metascore = scrapy.Field()
    movie_countries = scrapy.Field()
    movie_production_companies = scrapy.Field()
    movie_budget = scrapy.Field()
    movie_us_boxoffice = scrapy.Field()
    movie_boxoffice = scrapy.Field()
    movie_poster = scrapy.Field()