from ..items import ImdbOscarPageItem
from loguru import logger
from scrapy.spiders import CrawlSpider
from scrapy_selenium import SeleniumRequest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re

class ImdbOscarsSpider(CrawlSpider):
    name = "imdb_oscars"
    allowed_domains = ["www.imdb.com"]
    
    custom_settings = {
        'ITEM_PIPELINES': {"moviescraping.pipelines.OscarsPipeline": 100}
    }   
    
    @logger.catch
    def start_requests(self):
        # oscar_year_page_urls = [f'https://www.imdb.com/event/ev0000003/{year}/1' for year in range(2000, 2025, 1)]
        # for oscar_year_page_url in oscar_year_page_urls:
        #     yield SeleniumRequest(url=oscar_year_page_url,
        #                           wait_time=10,
        #                           callback=self.parse, # Callback argument tells to which function it has to send the info
        #     )      
        yield SeleniumRequest(url='https://www.imdb.com/event/ev0000003/2024/1',callback=self.parse)         
        
    
    @logger.catch
    def activate_ChromeDriver(self, response):
        
        # Define Options for ChromeDriver
        chrome_options = Options()
            # 1. Execute Chrome in headless mode (without graphic interface)
        chrome_options.add_argument("--headless")
            # 2. Desable GPU
        chrome_options.add_argument("--disable-gpu")
        
        # Activate ChromeDriver
        driver = webdriver.Chrome(options=chrome_options)
        
        # Load Url to ChromeDriver
        driver.get(response.url)
        return driver
        
    @logger.catch
    def parse(self, response):
        
        # Call Items
        imdb_oscar_item = ImdbOscarPageItem()
        # Activate ChromeDriver with response
        driver = self.activate_ChromeDriver(response)
        
        # Define URL Item
        imdb_oscar_item['url'] = response.url
        
        # Define Year Item
        imdb_oscar_item['year'] = (response.url)
        
        # Define Categories Item
            # 1. Scrap JS elements with CSS Selector 
        category_elements = driver.find_elements(By.CSS_SELECTOR, 'div.event-widgets__award-category div.event-widgets__award-category-name')
            # 2. Loop on each element to get every text
        categories = [element.text for element in category_elements]
            # 3. Assign categories to Item
        imdb_oscar_item['categories'] = categories
        
        # Scrap all nominees & winners for every category
        nominees_list = driver.find_elements(By.CSS_SELECTOR, 'div.event-widgets__award h3.event-widgets__award-categories div.event-widgets__award-category')
        nominees = [nominee.text for nominee in nominees_list]
        # Initialiser une liste pour stocker les gagnants
        all_winners = []
        # Utiliser une expression régulière pour extraire le gagnant
        pattern = r'WINNER,(.*?)'
        # Rechercher tous les matchs dans le texte
        winners = re.findall(pattern, nominees_list)
        # Ajouter les gagnants à l'élément imdb_oscar_item
        imdb_oscar_item['nominees'] = winners
        
        yield imdb_oscar_item