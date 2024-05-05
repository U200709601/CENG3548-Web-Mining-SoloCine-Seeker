import requests
from bs4 import BeautifulSoup
import pandas as pd

movie_dict = {'Ranking': [], 'Name': [], 'Year': [], 'Duration': [], 'Point': []}

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'}

response = requests.get('https://m.imdb.com/chart/top/', headers=headers)

html_text = response.text

soup = BeautifulSoup(html_text, 'lxml')

movie_list = soup.find_all('li', class_='cli-parent')

for movie in movie_list:
    movie_dict['Ranking'].append(movie.find('h3', class_='ipc-title__text').text.split('.')[0])
    movie_dict['Name'].append(movie.find('h3', class_='ipc-title__text').text.split('.')[1].strip())
    movie_dict['Year'].append(movie.find_all('span', class_='cli-title-metadata-item')[0].text)
    movie_dict['Duration'].append(movie.find_all('span', class_='cli-title-metadata-item')[1].text)
    movie_dict['Point'].append(movie.find('span', class_='ratingGroup--imdb-rating').text[0:3])

df = pd.DataFrame(movie_dict)
df.to_excel('top250.xlsx')