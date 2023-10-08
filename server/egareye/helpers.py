import paramiko
import requests
import random
import time
import os
from bs4 import BeautifulSoup
from egareye.constants import RUNNING, UPCOMING
from dotenv import load_dotenv


UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1", 
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
      )

# session for Cookie, Connection and Header persistence + maintain stateful inetraction

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

def monitorloop(movie, url_movie, freq, city):
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
            # notify
            break
        else:
            print('Bookings not yet open '+movie)
        n-=1
        time.sleep(freq)
        
def runOnVM(command):
    load_dotenv()

    host = os.getenv("MONITOR_VM_HOST")
    port = os.getenv("MONITOR_VM_PORT")  
    username = os.getenv("MONITOR_VM_USERNAME")
    password = os.getenv("MONITOR_VM_PASSWORD")  

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port=port, username=username, password=password, timeout=60)

        stdin, stdout, stderr = ssh.exec_command(command, timeout=60)

        print("Output of 'monitor.py' script:")
        print(stdout.read().decode())

    except Exception as e:
        print("An error occurred:", str(e))

    finally:
        if ssh is not None:
            ssh.close()