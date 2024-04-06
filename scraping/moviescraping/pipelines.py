# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class MoviescrapingPipeline:
    def process_item(self, item, spider):
        return item



from datetime import datetime
import locale
import sqlite3
    
class MoviesPipeline:
    def __init__(self) -> None:
        # connect to database
        self.con = sqlite3.connect('../data/movies.db')
        # create cursor to execute commands
        self.cur = self.con.cursor()
        # create table
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS upcoming_movies(
                             
                             movie_id TEXT,
                             movie_url TEXT,
                             year DATETIME,
                             movie_title TEXT,
                             movie_original_title TEXT,
                             movie_length TEXT,
                             movie_imdb_rating REAL,
                             movie_imdb_nb_of_ratings INTEGER,
                             movie_imdb_popularity INTEGER,
                             movie_synopsis TEXT,
                             movie_director TEXT,
                             movie_cast TEXT,
                             movie_categories TEXT,
                             movie_imdb_metascore INTEGER,
                             movie_countries TEXT,
                             movie_production_companies TEXT,
                             movie_budget TEXT,
                             movie_us_boxoffice INTEGER,
                             movie_boxoffice INTEGER
                             )
                             
                             """)    
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        
        for field_name in field_names:
            
            if field_name == "movie_id":
                movie_id = adapter.get('movie_url')
                if movie_id is not None:
                    movie_id = 'tt' + ''.join(filter(str.isdigit, movie_id))
                adapter['movie_id'] = movie_id
            
            if field_name == 'movie_url':
                url = adapter.get('movie_url')
                if url is not None:
                    url = str(url)
                adapter['movie_url'] = url
            
            elif field_name == 'year':
                year = adapter.get('year')
                if year is not None:
                    year = int(year)
                adapter["year"] = year
                
            elif field_name == 'movie_title':
                movie_title = adapter.get('movie_title')
                movie_title = str(movie_title).title()
                adapter['movie_title'] = movie_title
                
            elif field_name == 'movie_original_title':
                movie_original_title = adapter.get('movie_original_title')
                if movie_original_title is not None:
                    if "Original Title" in movie_original_title:
                        movie_original_title = movie_original_title[16:]
                    movie_original_title = str(movie_original_title).title()
                adapter['movie_original_title'] = movie_original_title
                
            elif field_name == 'movie_length':
                movie_length = adapter.get('movie_length')
                if movie_length is not None:
                    movie_length = str(movie_length)
                    if " " in movie_length:
                        movie_length = movie_length.split(' ')
                        if len(movie_length) > 1 and len(movie_length[1]) != 0 :
                            hours = int(''.join(filter(str.isdigit, movie_length[0])))
                            minutes = int(''.join(filter(str.isdigit, movie_length[1])))
                            movie_length = int((hours * 60) + minutes)
                        else:
                            if "min" in movie_length:
                                movie_length = int(''.join(filter(str.isdigit, movie_length[0])))
                            elif "h" in movie_length:
                                hours = int(''.join(filter(str.isdigit, movie_length[0])))
                                movie_length = int(hours*60)
                    else:
                        if "min" in movie_length or "m" in movie_length:
                            minutes = int(''.join(filter(str.isdigit, movie_length)))
                            movie_length = minutes
                        elif "h" in movie_length:
                            hours = int(''.join(filter(str.isdigit, movie_length)))
                            movie_length = int(hours * 60)
                adapter['movie_length'] = movie_length
                
            elif field_name == 'movie_imdb_rating':
                movie_imdb_rating = adapter.get('movie_imdb_rating')
                if movie_imdb_rating is not None:
                    movie_imdb_rating = str(movie_imdb_rating).replace(',', ".")
                    movie_imdb_rating = float(movie_imdb_rating)
                adapter['movie_imdb_rating'] = movie_imdb_rating
                
            elif field_name == 'movie_imdb_nb_of_ratings':
                movie_imdb_nb_of_ratings = adapter.get('movie_imdb_nb_of_ratings')
                if movie_imdb_nb_of_ratings is not None:
                    # Convert 1K to 1 000
                    if "k" in movie_imdb_nb_of_ratings or "K" in movie_imdb_nb_of_ratings:
                        movie_imdb_nb_of_ratings = int(''.join(filter(str.isdigit, movie_imdb_nb_of_ratings))) * 1000
                    # Convert 1M to 1 000 000
                    elif "M" in movie_imdb_nb_of_ratings:
                        movie_imdb_nb_of_ratings = int(''.join(filter(str.isdigit, movie_imdb_nb_of_ratings))) * 1000000
                    movie_imdb_nb_of_ratings = int(movie_imdb_nb_of_ratings)
                adapter['movie_imdb_nb_of_ratings'] = movie_imdb_nb_of_ratings
                
            elif field_name == 'movie_imdb_popularity':
                movie_imdb_popularity = adapter.get('movie_imdb_popularity')
                if movie_imdb_popularity is not None:
                    movie_imdb_popularity = ''.join(filter(str.isdigit, movie_imdb_popularity))
                    movie_imdb_popularity = int(movie_imdb_popularity)
                adapter['movie_imdb_popularity'] = movie_imdb_popularity
                
            elif field_name == 'movie_synopsis':
                movie_synopsis = adapter.get('movie_synopsis')
                if movie_synopsis is not None:
                    movie_synopsis = str(movie_synopsis)
                adapter['movie_synopsis'] = movie_synopsis
                
            elif field_name == 'movie_director':
                movie_director = adapter.get('movie_director')
                if movie_director is not None:
                    movie_director = str(movie_director)
                    movie_director = ''.join(movie_director.replace("[", "").replace("]", "").replace("'", ""))
                    if "," in movie_director:
                        movie_director = movie_director.replace(', ', '|')
                adapter['movie_director'] = movie_director
                
            elif field_name == 'movie_cast':
                movie_cast = adapter.get('movie_cast')
                if movie_cast is not None:
                    movie_cast = str(movie_cast)
                    movie_cast = ''.join(movie_cast.replace("[", "").replace("]", "").replace("'", ""))
                    movie_cast = movie_cast.replace(', ', '|')
                adapter['movie_cast'] = movie_cast
                
            elif field_name == 'movie_categories':
                movie_categories = adapter.get('movie_categories')
                if movie_categories is not None:
                    movie_categories = str(movie_categories)
                    movie_categories = ''.join(movie_categories.replace("[", "").replace("]", "").replace("'", ""))
                    movie_categories = movie_categories.replace(', ', '|')
                adapter['movie_categories'] = movie_categories
                
            elif field_name == 'movie_imdb_metascore':
                movie_imdb_metascore = adapter.get('movie_imdb_metascore')
                if movie_imdb_metascore is not None:
                    movie_imdb_metascore = int(movie_imdb_metascore)
                adapter['movie_imdb_metascore'] = movie_imdb_metascore
                
            elif field_name == 'movie_countries':
                movie_countries = adapter.get('movie_countries')
                if movie_countries is not None:
                    movie_countries = str(movie_countries)
                    movie_countries = ''.join(movie_countries.replace("[", "").replace("]", "").replace("'", ""))
                    movie_countries = movie_countries.replace(', ', '|')
                adapter['movie_countries'] = movie_countries        
                
            elif field_name == 'movie_production_companies':
                movie_production_companies = adapter.get('movie_production_companies')
                if movie_production_companies is not None:
                    movie_production_companies = str(movie_production_companies)
                    movie_production_companies = ''.join(movie_production_companies.replace("[", "").replace("]", "").replace("'", ""))
                    movie_production_companies = movie_production_companies.replace(', ', '|')
                adapter['movie_production_companies'] = movie_production_companies
                
            elif field_name == 'movie_budget':
                movie_budget = adapter.get('movie_budget')
                if movie_budget is not None:
                    movie_budget = str(movie_budget)
                    if "(estimé)" in movie_budget:
                        movie_budget = movie_budget.replace("(estimé)", "")
                    
                    # currencies = {
                    #     '$US' : 1,
                    #     '$CA' : 1.36,
                    #     '€' : 1.09,
                    #     'RUR' : 0.92,
                    #     '₩' : 0.00075,
                    #     '£' : 1.27,
                    #     '₹' : 0.012
                    # }
                    
                    # for currency, value in currencies.items():
                    #     if currency in str(movie_budget):
                    #         movie_budget = int(''.join(filter(str.isdigit, str(movie_budget)))) * value
                                
                    # movie_budget = int(''.join(filter(str.isdigit, str(movie_budget))))
                    # movie_budget = str(movie_budget)
                adapter['movie_budget'] = movie_budget
                
            elif field_name == 'movie_us_boxoffice':
                movie_us_boxoffice = adapter.get('movie_us_boxoffice')
                if movie_us_boxoffice is not None:
                    movie_us_boxoffice = str(movie_us_boxoffice)
                    if "\u202f" in movie_us_boxoffice:
                        movie_us_boxoffice = movie_us_boxoffice.replace("\u202f", "")
                    if "\xa0$US" in movie_us_boxoffice:
                        movie_us_boxoffice = movie_us_boxoffice.replace("\xa0$US", "")
                    if " $US" in movie_us_boxoffice:
                        movie_us_boxoffice = movie_us_boxoffice.replace(" $US", "")
                    movie_us_boxoffice = int(''.join(filter(str.isdigit, movie_us_boxoffice)))
                adapter['movie_us_boxoffice'] = movie_us_boxoffice
                
            elif field_name == 'movie_boxoffice':
                movie_boxoffice = adapter.get('movie_boxoffice')
                if movie_boxoffice is not None:
                    movie_boxoffice = str(movie_boxoffice)
                    if "\u202f" in movie_boxoffice:
                        movie_boxoffice = movie_boxoffice.replace("\u202f", "")
                    if "\xa0$US" in movie_boxoffice:
                        movie_boxoffice = movie_boxoffice.replace("\xa0$US", "")
                    if "$US" in movie_boxoffice:
                        movie_boxoffice = movie_boxoffice.replace("$US", "")
                    movie_boxoffice = int(''.join(filter(str.isdigit, movie_boxoffice)))
                adapter['movie_boxoffice'] = movie_boxoffice         

                         
            
        self.cur.execute("""
                         INSERT INTO upcoming_movies (movie_id, movie_url, year, movie_title, movie_original_title, movie_length, movie_imdb_rating, movie_imdb_nb_of_ratings, movie_imdb_popularity, movie_synopsis, movie_director, movie_cast, movie_categories, movie_imdb_metascore, movie_countries, movie_production_companies, movie_budget, movie_us_boxoffice, movie_boxoffice) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                         """,
                         
                         (
                             adapter["movie_id"],
                             adapter['movie_url'],
                             adapter['year'],
                             adapter['movie_title'],
                             adapter['movie_original_title'],
                             adapter["movie_length"],
                             adapter['movie_imdb_rating'],
                             adapter['movie_imdb_nb_of_ratings'],
                             adapter['movie_imdb_popularity'],
                             adapter["movie_synopsis"],
                             adapter['movie_director'],
                             adapter['movie_cast'],
                             adapter['movie_categories'],
                             adapter['movie_imdb_metascore'],
                             adapter["movie_countries"],
                             adapter['movie_production_companies'],
                             adapter['movie_budget'],
                             adapter['movie_us_boxoffice'],
                             adapter['movie_boxoffice'],
                             
                             
                         )
                         
                         )
        
        self.con.commit()
        
        # self.cur.execute("""
        #                 CREATE TABLE IF NOT EXISTS upcoming_movies_categories(
                            
        #                     category TEXT UNIQUE
        #                     )
                            
        #                     """)
        
        # # Loop on every modified category from the modified_categ list & insert data into table
        #     # 1. Clean data accordingly  
        # catset = adapter.get('movie_categories') 
        # catset = str(catset)
        # catset = movie_categories.split(",")
        #     # 2. Insert data into DB
        # for cat in catset:
        #     self.cur.execute("""
        #                         INSERT OR IGNORE INTO upcoming_movies_categories (category) VALUES (?)
        #                         """,
        #                         (
        #                             cat,
        #                         ))
        
        # self.con.commit()
        
        
        # self.cur.execute("""
        #                 CREATE TABLE IF NOT EXISTS upcoming_movies_countries(
                            
        #                     country TEXT UNIQUE
        #                     )
                            
        #                     """)
        
        # # Loop on every modified country from the modified_categ list & insert data into table
        #     # 1. Clean data accordingly  
        # countries = adapter.get('movie_countries') 
        # countries = str(countries)
        # countries = countries.split(",")
        #     # 2. Insert data into DB
        # for country in countries:
        #     self.cur.execute("""
        #                         INSERT OR IGNORE INTO upcoming_movies_countries (country) VALUES (?)
        #                         """,
        #                         (
        #                             country,
        #                         ))
        
        # self.con.commit()
                    
        return item
    
class OscarsPipeline:
    def __init__(self) -> None:
        # create database
        self.con = sqlite3.connect('../data/movies.db')
        # create cursor to execute commands
        self.cur = self.con.cursor()
        # create table
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS oscars(
                             
                             id INTEGER PRIMARY KEY AUTOINCREMENT,
                             url TEXT,
                             year TEXT,
                             categories TEXT,
                             winners TEXT
                             )
                             
                             """)    
    
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        
        field_names = adapter.field_names()
        
        for field_name in field_names:
            
            if field_name == 'url':
                url = adapter.get('url')
                if url is not None:
                    url = str(url)
                adapter['url'] = url
            
            elif field_name == 'year':
                year = adapter.get('year')
                year = str(year)
                year = ''.join(filter(str.isdigit, year))
                year = year[-5:-1]
                adapter["year"] = int(year)
                
            elif field_name == 'categories':
                categories = adapter.get('categories')
                categories = str(categories)
                categ = categories.split("', '")
                
                modified_categ = []

                for element in categ:
                    if "['" in element:
                        element = element.replace("['", "")
                    elif "']" in element:
                        element = element.replace("']", "")
                    
                    # Add the modified (or not) element to the empty list declared before the for loop
                    modified_categ.append(element)
                
                modified_categ = str(modified_categ).replace('[', '').replace(']', '')
                
                adapter['categories'] = str(modified_categ)
                
            # elif field_name == 'nominees':
            #     nominees = adapter.get('nominees')
            #     if nominees is not None:
            #         try:
            #             nominees = [str(nominee).replace('\\n', ',') for nominee in nominees]
            #             nominees = str(nominees)
            #         except Exception as e:
            #             nominees = str(nominees)
            #     adapter['nominees'] = nominees
                
            elif field_name == 'winners':
                winners = adapter.get('winners')
                if winners is not None:
                    try:
                        winners = [str(winner).replace('\\n', ',') for winner in winners]
                        winners = winners.replace("\\", '')
                    except Exception as e:
                        winners = str(winners)
                adapter['winners'] = winners
        
        self.cur.execute("""
                         INSERT INTO oscars (url, year, categories, winners) VALUES (?, ?, ?, ?)
                         """,
                         
                         (
                             adapter['url'],
                             adapter['year'],
                             adapter['categories'],
                             adapter['winners'],
                         )
                         
                         )
        
        self.con.commit()
        
        self.cur.execute("""
                         CREATE TABLE IF NOT EXISTS oscars_categories(
                             
                             category TEXT UNIQUE
                             
                             )
                             """)

        # Loop on every modified category from the modified_categ list & insert data into table
        catset = set(modified_categ)
        for cat in catset:
            self.cur.execute("""
                                    INSERT OR IGNORE INTO oscars_categories (category) VALUES (?)
                                    """,
                                    (
                                        cat,
                                    ))
        
        self.con.commit()
                    
        return item
    