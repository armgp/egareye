import os
import sys
import plivo
import requests
import random
import json
import time
import psutil
from bs4 import BeautifulSoup
from dotenv import load_dotenv

UAS = ("Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1", 
        "Mozilla/5.0 (Windows NT 6.3; rv:36.0) Gecko/20100101 Firefox/36.0",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.0 Safari/537.36",
      )

phoneNumbersPath = '/home/gp/Documents/Dev/plivo/monitor_script/phoneNumbers.json'
processIdPath = '/home/gp/Documents/Dev/plivo/monitor_script/processId.json'

def makeCall(movie, city):
    load_dotenv()
    auth_id    = os.getenv("AUTH_ID")
    auth_token = os.getenv("AUTH_TOKEN")
    client = plivo.RestClient(auth_id,auth_token)

    response = client.numbers.list(limit=5, offset=0)
    # response = client.numbers.search(country_iso='GB')
    number = next(numberData['number'] for numberData in response if numberData['voice_enabled'] == True)
    # response = client.numbers.buy(number)
    print("Call from", number)

    with open(phoneNumbersPath) as file:
        data = json.load(file)

    key = movie+"-"+city
    client_number = ""
    for phnNo in data[key]:
        client_number=client_number+phnNo+"<"
    client_number = client_number[:-1]
    print(client_number)

    response = client.calls.create(
        from_=number,
        to_=client_number,
        # to_ = '+917012496675<+917907914941',
        answer_url='https://s3.amazonaws.com/static.plivo.com/answer.xml',
        # answer_url='https://static.staticsave.com/plivo/answer.xml',
        # fallback_url='https://s3.amazonaws.com/static.plivo.com/answer.xml',
        answer_method='GET', )
    print(response)
    # client.numbers.delete(number)

if len(sys.argv) < 4:
    print("Usage: python3 monitor.py <movie> <city> <url_movie>")
    print("Eg: python3 monitor.py leo 5 hyderabad +919999999999")
else:
    movie = sys.argv[1]
    city = sys.argv[2]
    url_movie = sys.argv[3]

session = requests.Session()  
ua = UAS[random.randrange(len(UAS))]
session.headers.update({'user-agent': ua})
url = "https://ticketnew.com/movies/"+city
session.get(url)

while(True):
    response = session.get(url_movie)
    soup = BeautifulSoup(response.content, "html.parser")
    showlisting = soup.find('a', string='Showlisting')
    if(showlisting):
        print("Bookings Open for "+movie)
        makeCall(movie, city)
        with open(phoneNumbersPath) as file:
                data = json.load(file)
        key = movie+"-"+city
        del data[key]
        with open(phoneNumbersPath, 'w') as file:
            json.dump(data, file)
        break
    else:
        print('Bookings not yet open '+movie)
    time.sleep(5)


key = movie+"-"+city
with open(processIdPath) as file:
    processData = json.load(file)
del processData[key]
with open(processIdPath, 'w') as file:
    json.dump(processData, file)