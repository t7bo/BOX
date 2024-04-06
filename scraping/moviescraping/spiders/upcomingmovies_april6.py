import scrapy
from ..items import UpcomingMovieItem



class ImdbUpcomingMoviesSpider(scrapy.Spider):
    name = "upcomingmovies_april6"
    allowed_domains = ["www.imdb.com"]
    start_urls = ["https://www.imdb.com/calendar/"]
    
    custom_settings = {
        'ITEM_PIPELINES': {"moviescraping.pipelines.UpcomingMoviesPipeline": 100}
    }   
    
    def parse(self, response):
        
        upcoming_movies = response.css('li[data-testid="coming-soon-entry"]')

        for movie in upcoming_movies:    
            relative_url = movie.css('a.ipc-metadata-list-summary-item__t::attr(href)').get()
            movie_url = 'https://www.imdb.com' + relative_url
            yield response.follow(movie_url, callback=self.parse_movie_page)

    def parse_movie_page(self, response):
        
        upcoming_movie_item = UpcomingMovieItem()
        
        upcoming_movie_item['movie_url'] = response.url
        upcoming_movie_item['movie_id'] = response.url
        upcoming_movie_item['release_date'] = response.xpath('//li[@data-testid="title-details-releasedate"]/div/ul/li/a/text()').get()
        upcoming_movie_item['movie_title'] = response.xpath('//span[@data-testid="hero__primary-text"]/text()').get()
        upcoming_movie_item['movie_original_title'] = response.xpath('//h1[@data-testid="hero__pageTitle"]/following-sibling::div/text()').get()
        upcoming_movie_item["movie_length"] = response.css('li[role="presentation"]::text').get()
        upcoming_movie_item['movie_imdb_rating'] = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]/span/text()').get()
        upcoming_movie_item['movie_imdb_nb_of_ratings'] = response.xpath('//div[@data-testid="hero-rating-bar__aggregate-rating__score"]//following-sibling::div/text()').get()
        upcoming_movie_item['movie_imdb_popularity'] = response.xpath('//div[@data-testid="hero-rating-bar__popularity__score"]/text()').get()
        upcoming_movie_item['movie_synopsis'] = response.xpath('//span[@data-testid="plot-l"]/text()').get()
        upcoming_movie_item['movie_director'] = response.xpath('//section[1]/section/div[3]/section/section/div[3]/div[2]/div[1]/section/div[2]/div/ul/li[1]/div/ul/li/a/text()').getall()
        upcoming_movie_item['movie_cast'] = response.xpath('//a[@data-testid="title-cast-item__actor"]/text()').getall()
        upcoming_movie_item['movie_categories'] = response.xpath('//div[@class="ipc-chip-list__scroller"]/a/span[@class="ipc-chip__text"]/text()').getall()
        upcoming_movie_item['movie_imdb_metascore'] = response.css('span.metacritic-score-box::text').get()
        upcoming_movie_item['movie_countries'] = response.xpath('//li[@data-testid="title-details-origin"]/div/ul/li/a/text()').getall()
        upcoming_movie_item['movie_production_companies'] = response.xpath('//li[@data-testid="title-details-companies"]/div/ul/li/a/text()').getall()
        upcoming_movie_item['movie_budget'] = response.xpath('//li[@data-testid="title-boxoffice-budget"]/div/ul/li/span/text()').get()
        upcoming_movie_item['movie_us_boxoffice'] = response.xpath('//li[@data-testid="title-boxoffice-grossdomestic"]/div/ul/li/span/text()').get()
        upcoming_movie_item['movie_boxoffice'] = response.xpath('//li[@data-testid="title-boxoffice-cumulativeworldwidegross"]/div/ul/li/span/text()').get()
        
        poster_url = response.css('a.ipc-lockup-overlay::attr(href)').get()
        if poster_url:
            yield response.follow('https://www.imdb.com' + poster_url, callback=self.parse_poster_page, meta={'upcoming_movie_item': upcoming_movie_item})
        else:
            yield upcoming_movie_item
            
    def parse_poster_page(self, response):
        upcoming_movie_item = response.meta['upcoming_movie_item']
        upcoming_movie_item['movie_poster'] = response.xpath('//img[@class="sc-7c0a9e7c-0 eWmrns"]/@src').get()
        yield upcoming_movie_item