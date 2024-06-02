import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
from bs4 import BeautifulSoup 
import os
from selenium.webdriver.chrome.options import Options

class IMDbSpider(scrapy.Spider):
    name = 'imdb_spider'
    start_urls = ['https://m.imdb.com/chart/top/?language=en-US']
    
    def __init__(self):
        chrome_options = Options()
        chrome_options.add_experimental_option('prefs', {'intl.accept_languages': 'en-US'})
        self.driver = webdriver.Chrome(options=chrome_options)


    def parse(self, response):
        self.driver.get(response.url)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "cli-parent")))

        movie_dict = {'Ranking': [], 'Name': [], 'Year': [], 'Duration': [], 'Point': []}

        while len(movie_dict['Ranking']) < 250:
            html = self.driver.page_source
            soup = BeautifulSoup(html, 'html.parser')

            movie_list = soup.find_all('li', class_='cli-parent')
            for movie in movie_list:
                movie_dict['Ranking'].append(movie.find('h3', class_='ipc-title__text').text.split('.')[0])
                movie_dict['Name'].append(movie.find('h3', class_='ipc-title__text').text.split('.')[1].strip())
                movie_dict['Year'].append(movie.find_all('span', class_='cli-title-metadata-item')[0].text)
                movie_dict['Duration'].append(movie.find_all('span', class_='cli-title-metadata-item')[1].text)
                movie_dict['Point'].append(movie.find('span', class_='ratingGroup--imdb-rating').text[0:3])

            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2)

        self.driver.quit()

        df = pd.DataFrame(movie_dict)
        csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))), 'data', 'movies.csv')
        os.makedirs(os.path.dirname(csv_path), exist_ok=True)
        df.to_csv(csv_path, index=False)
        self.log(f"Data has been written to {csv_path}")

        yield {
            'movie_data': df.to_dict(orient='records')
        }
