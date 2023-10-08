import os
import sys
import plivo
import requests
import random
import time
from bs4 import BeautifulSoup
from dotenv import load_dotenv

UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1", 
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
      )

RUNNING = 1
UPCOMING = 0

def getMovies(city, status):
    session = requests.Session()  
    ua = UAS[random.randrange(len(UAS))]
    session.headers.update({'user-agent': ua})

    if(status == RUNNING): url = "https://ticketnew.com/movies/"+city
    elif(status == UPCOMING): url = "https://ticketnew.com/movies/upcoming-movies?city="+city

    response = session.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    movie_links = soup.find_all('a', href=lambda href: href and href.startswith("/movies/") and "-movie-detail" in href)
    movie_links_urls = [link['href'] for link in movie_links]
    
    return movie_links_urls

def getMovieLink(movie_name, movie_urls):
    # movies = [url for url in movie_urls if url.startswith("/movies/"+movie_name+"-")]
    movie_link = next((link for link in movie_urls if link.startswith("/movies/"+movie_name+"-")), None)
    if(movie_link): return "https://ticketnew.com"+movie_link
    return None

def makeCall(client_number):
    load_dotenv()
    auth_id    = os.getenv("AUTH_ID")
    auth_token = os.getenv("AUTH_TOKEN")
    client = plivo.RestClient(auth_id,auth_token)

    response = client.numbers.list(limit=5, offset=0)
    # response = client.numbers.search(country_iso='GB')
    number = next(numberData['number'] for numberData in response if numberData['voice_enabled'] == True)
    # response = client.numbers.buy(number)
    print("Call from", number)

    response = client.calls.create(
        from_=number,
        to_=client_number,
        answer_url='https://s3.amazonaws.com/static.plivo.com/answer.xml',
        # answer_url='https://static.staticsave.com/plivo/answer.xml',
        # fallback_url='https://s3.amazonaws.com/static.plivo.com/answer.xml',
        answer_method='GET', )
    print(response)
    # client.numbers.delete(number)

def monitorloop(movie, url_movie, freq, city, phnNo):
    session = requests.Session()  
    ua = UAS[random.randrange(len(UAS))]
    session.headers.update({'user-agent': ua})
    url = "https://ticketnew.com/movies/"+city
    session.get(url)

    n=1
    while(n):
        response = session.get(url_movie)
        soup = BeautifulSoup(response.content, "html.parser")
        showlisting = soup.find('a', string='Showlisting')
        if(showlisting):
            print("Bookings Open for "+movie)
            makeCall(phnNo)
            break
        else:
            print('Bookings not yet open '+movie)
        n-=1
        time.sleep(freq)

def monitor(movie, freq, city, phnNo):
    running_movies = getMovies(city, RUNNING)
    upcoming_movies = getMovies(city, UPCOMING)

    url_movie = getMovieLink(movie, running_movies)
    if(url_movie == None): 
        url_movie = getMovieLink(movie, upcoming_movies)

    if(url_movie == None): 
        print(movie+" not found")
    else:
        monitorloop(movie, url_movie, freq, city, phnNo)

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python monitor.py <movie> <frequncy for monitoring in seconds> <city> <phnNo>")
        print("Eg: python3 monitor.py leo 5 hyderabad +919999999999")
    else:
        movie = sys.argv[1]
        freq = int(sys.argv[2])
        city = sys.argv[3]
        phnNo = sys.argv[4]
        monitor(movie, freq, city, phnNo)