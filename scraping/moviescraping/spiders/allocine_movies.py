from typing import Iterable
import scrapy
import time
from loguru import logger
from scrapy.spiders import CrawlSpider
from selenium import webdriver
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC

class AllocineMoviesSpider(CrawlSpider):
    name = "allocine_movies"
    allowed_domains = ["www.allocine.fr"]
    chrome_options = Options()
    chrome_options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=chrome_options)
    URLs = []
    
    def start_requests(self):
        url = "https://www.allocine.fr/films/decennie-2020/annee-2027/?page=1"
        yield scrapy.Request(url=url, callback=self.next_page) 
        
    @logger.catch    
    def next_page(self, response):
        
        self.driver.get(response.url)
        
        try: # Accept cookies
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
            accept_cookies.click()
            time.sleep(3)
        except Exception as e:
            pass    
        try: # Pass Ads
            time.sleep(3)
            pass_ad_button = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
            pass_ad_button.click()
        except Exception as e:
            pass        

        self.URLs.append(response.url)
        
        time.sleep(3)
        try:
            nextpage = self.driver.find_element(By.CSS_SELECTOR, 'a.button-right')
            next_url = nextpage.get_attribute('href')
            yield SeleniumRequest(url=next_url, callback=self.next_page)
        except Exception as e:
            for url in self.URLs:
                yield SeleniumRequest(url=url, callback=self.parse)
        
    @logger.catch
    def parse(self, response):
        
        self.driver.get(response.url)    
        
        try: # Accept cookies
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
            accept_cookies.click()
            time.sleep(3)
        except Exception as e:
            pass    
        try: # Pass Ads
            time.sleep(3)
            pass_ad_button = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
            pass_ad_button.click()
        except Exception as e:
            pass        
        
        # Collect all movies urls from one page
        movie_urls = self.driver.find_elements(By.CSS_SELECTOR, 'a.meta-title-link')
        for movie_url in movie_urls:
            movie_url = movie_url.get_attribute('href')
            yield scrapy.Request(url=movie_url, callback=self.parse_movie_page)
        
    @logger.catch
    def parse_movie_page(self, response):
        
        self.driver.get(response.url)
        
        try: # Accept cookies
            accept_cookies = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
            accept_cookies.click()
            time.sleep(3)
        except Exception as e:
            pass    
        try: # Pass Ads
            time.sleep(3)
            pass_ad_button = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
            pass_ad_button.click()
        except Exception as e:
            pass        
        
        movie_title = self.driver.find_element(By.CSS_SELECTOR, 'div.titlebar-title-xl')
        
        yield {
            'movie_url' : response.url,
            'movie_title' : movie_title.text
        }
        
    
    # def accept_cookies(self, response):
    #     self.driver.get(response.url)
    #     try: # Accept cookies
    #         accept_cookies = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
    #         accept_cookies.click()
    #         time.sleep(3)
    #     except Exception as e:
    #         pass    
        
    # def pass_ads(self, response):
    #     self.driver.get(response.url)
    #     try: # Accept cookies
    #         accept_cookies = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
    #         accept_cookies.click()
    #         time.sleep(3)
    #     except Exception as e:
    #         pass    
    #     try: # Pass Ads
    #         time.sleep(3)
    #         pass_ad_button = self.driver.find_element(By.XPATH, '//button[@onclick="Didomi.setUserAgreeToAll();"]')
    #         pass_ad_button.click()
    #     except Exception as e:
    #         pass           