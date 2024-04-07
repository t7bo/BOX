import scrapy
import time
from loguru import logger
from scrapy.spiders import CrawlSpider
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import re

class ImdbMoviesSpider(CrawlSpider):
    name = "imdb_movies_id"
    allowed_domains = ["www.imdb.com"]
    driver = webdriver.Chrome()
    
    custom_settings = {
        'DOWNLOADER_MIDDLEWARES': {
            'moviescraping.middlewares.CustomMiddleware': 400,
        },
    }
        
    def start_requests(self): # URL -> french audio movies (no documentaries, no shorts) from 2021 to 2025
        url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2000-01-01,&genres=!documentary,!short&primary_language=fr,en&sound_mixes=dolby_digital"
        yield SeleniumRequest(url=url, callback=self.parse)

    @logger.catch
    def parse(self, response):
        
        # 1) Reject Cookies if pop-up emerges
        self.driver.get(response.url)
        time.sleep(5)
        reject_cookies = self.driver.find_element(By.XPATH, '//*[@id="__next"]/div/div/div[2]/div/button[1]')
        reject_cookies.click()
        time.sleep(5)
        
        # 2) Check if there is a "see more" button
        try:
            while True:
                button = self.driver.find_element(By.XPATH, '//main/div[2]/div[3]/section/section/div/section/section/div[2]/div/section/div[2]/div[2]/div[2]/div/span/button')

                # Scroll down the page until you get to the element using JavaScript
                self.driver.execute_script("arguments[0].scrollIntoView();", button)
                # If there's a button "see more" -> click on it
                time.sleep(3)
                button.click()
                time.sleep(3)
        except NoSuchElementException:
            pass
        
        # 3) When the page is entirely loaded -> Get all movie urls
        movie_links = self.driver.find_elements(By.CSS_SELECTOR, 'a.ipc-title-link-wrapper')
        for link in movie_links:
            movie_url = link.get_attribute('href')
            # yield scrapy.Request(url=movie_url, callback=self.parse_movie_page)
            yield SeleniumRequest(url=movie_url, callback=self.parse_movie_page)

    @logger.catch
    def parse_movie_page(self, response):
        yield {
            'movie_url': response.url,
            'movie_id': re.search(r'tt\d+', str(response.url)).group()
        }
