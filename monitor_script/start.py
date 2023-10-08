import os
import sys
import plivo
import requests
import random
import json
import time
import psutil
import subprocess
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

def isProcessRunning(process_id):
    try:
        process = psutil.Process(process_id)
        return process.is_running()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
        return False

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

def monitor(movie, freq, city):
    running_movies = getMovies(city, RUNNING)
    upcoming_movies = getMovies(city, UPCOMING)

    url_movie = getMovieLink(movie, running_movies)
    if(url_movie == None): 
        url_movie = getMovieLink(movie, upcoming_movies)

    if(url_movie == None): 
        print(movie+" not found")
        return -1
    else:
        try:
            print('python3', '/home/gp/Documents/Dev/plivo/monitor_script/monitor.py', movie, freq, city, url_movie)
            process = subprocess.Popen(['python3', '/home/gp/Documents/Dev/plivo/monitor_script/monitor.py', movie, freq, city, url_movie],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE,
                                   close_fds=True, preexec_fn=os.setsid)
            process_id = process.pid
            return process_id
        except Exception as e:
            print("Error : ", e)
            return -1

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python3 start.py <movie> <frequency for monitoring in seconds> <city> <phnNo>")
        print("Eg: python3 start.py leo 5 hyderabad +919999999999")
    else:
        movie = sys.argv[1]
        freq = sys.argv[2]
        city = sys.argv[3]
        phnNo = sys.argv[4]

        phoneNumbersPath = '/home/gp/Documents/Dev/plivo/monitor_script/phoneNumbers.json'
        processIdPath = '/home/gp/Documents/Dev/plivo/monitor_script/processId.json'

        with open(phoneNumbersPath, 'r') as file:
            data = json.load(file)

        key = movie+"-"+city
        if key in data:
            numbers = set(data[key])
            numbers.add(phnNo)
            data[key] = list(numbers)
        else: data[key] = [phnNo]

        with open(phoneNumbersPath, 'w') as file:
            json.dump(data, file)

        with open(processIdPath) as file:
            processData = json.load(file)

        if key in processData:
            pid = processData[key]
            if not isProcessRunning(pid):
                pid = monitor(movie, freq, city)
                if pid != -1:
                    processData[key] = pid
        else:
            pid = monitor(movie, freq, city)
            if pid != -1:
                processData[key] = pid

        with open(processIdPath, 'w') as file:
            json.dump(processData, file)

# python3 monitor.py <movie> <frequency for monitoring in seconds> <city> <url_movie>