import requests
from bs4 import BeautifulSoup 

page = requests.get('https://www.imdb.com/chart/top')
soup = BeautifulSoup(page.content, 'html.parser')
all_movies = soup.find(class_='lister-list')


for i in range(0,250):
    
    movie = all_movies.find_all(class_="titleColumn")[i]
    rate = all_movies.find_all(class_="ratingColumn imdbRating")[i]
    print("Movie: {}  |   IMDb Rate:{}".format(" ".join(movie.get_text().split()), " ".join(rate.get_text().split())))