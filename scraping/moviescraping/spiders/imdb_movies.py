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
    name = "imdb_movies"
    allowed_domains = ["www.imdb.com"]
    driver = webdriver.Chrome()
        
    def start_requests(self): # URL -> french audio movies (no documentaries, no shorts) from 2021 to 2025
        url = "https://www.imdb.com/search/title/?title_type=feature&release_date=2021-05-19,2024-12-31&genres=!documentary,!short&languages=fr"
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
                time.sleep(3) # wait 2s
                # If there's a button "see more" -> click on it
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
        
        data = response.meta.get('data')
        
        # Reload driver with the movie url
        self.driver.get(response.url)
        
        # Scrap all the information from every movie page
        movie_title = self.driver.find_element(By.XPATH, '//span[@data-testid="hero__primary-text"]')
        # original_title = self.driver.find_element(By.XPATH, '//main/div/section[1]/section/div[3]/section/section/div[2]/div[1]/div')
        # release_date = self.driver.find_element(By.XPATH, '//a[@class="ipc-metadata-list-item__list-content-item ipc-metadata-list-item__list-content-item--link"]')
        
        yield {
            'movie_url': response.url,
            'movie_id': re.search(r'tt\d+', str(response.url)).group(),
            'movie_title' : movie_title.text,
            # 'original_title' : original_title.text,
            # 'release_date' : release_date.text
            
        }
