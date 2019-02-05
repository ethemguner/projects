import requests
from bs4 import BeautifulSoup
import sqlite3     

## Parse process
page = requests.get('https://www.imdb.com/chart/top')
soup = BeautifulSoup(page.content, 'html.parser')
page_content = soup.find(class_='lister-list') ## find the list

## creating database
conn = sqlite3.connect("movieDatabase.db")
cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS movies (movie_name TEXT, imdb_rate INT)")

## a for loop. goes 250 for 250 movies.
for i in range(0,250):
    
    ## catching movie name, year, place
    movie = page_content.find_all(class_="titleColumn")[i]
    print("Movie: {}".format(" ".join(movie.get_text().split())))
    ## catching imdbrate
    rate = page_content.find_all(class_="ratingColumn imdbRating")[i]
    print("Rate: {}\n".format(" ".join(rate.get_text().split())))
    ## insert to database
    cursor.execute("INSERT INTO movies VALUES(?,?)",(" ".join(movie.get_text().split()), 
                                              " ".join(rate.get_text().split())))  ## " ".join(sentence.split()) delete the duplicate spaces.
    conn.commit()
    
    