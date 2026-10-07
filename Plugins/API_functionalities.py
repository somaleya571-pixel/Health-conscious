import os
import datetime
from dotenv import load_dotenv
try:
    from newsapi import NewsApiClient
except ImportError:
    NewsApiClient = None
import re
import requests
try:
    from wolframalpha import Client
except ImportError:
    Client = None

env_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'Data', '.env'))
load_dotenv(dotenv_path=env_path)

NEWS = os.getenv('NEWS_API')
WOLFRAMALPHA = os.getenv('WOLFRAMALPHA_API')
OPENWEATHERMAP = os.getenv('OPENWEATHERMAP_API')
TMDB = os.getenv('TMDB_API')
news = NewsApiClient(api_key=NEWS) if NewsApiClient and NEWS else None

def get_ip(_return=False):
    try:
        response = requests.get(f'http://ip-api.com/json/').json()
        if _return:
            return response
        else:
            return f'Your IP address is {response["query"]}'
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

def get_joke():
    try:
        joke = requests.get('https://v2.jokeapi.dev/joke/Any?format=txt').text
        return joke
    except KeyboardInterrupt:
        return None
    except requests.exceptions.RequestException:
        return None

def get_news():
    if not news:
        return None
    try:
        top_news = ""
        top_headlines = news.get_top_headlines(language="en", country="in")
        for i in range(10):
             top_news += re.sub(r'[|-] [A-Za-z0-9 |:.]*', '', top_headlines['articles'][i]['title']).replace("’", "'") + '\n'
        return top_news
    except KeyboardInterrupt:
        return None
    except Exception:
        return None

def get_weather(city=''):
    try:
        if city:
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP}&units=metric').json()
        else:
            response = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={get_ip(True)["city"]}&appid={OPENWEATHERMAP}&units=metric').json()
        weather = f'It\'s {response["main"]["temp"]}° Celsius and {response["weather"][0]["main"]}\n' \
               f'But feels like {response["main"]["feels_like"]}° Celsius\n' \
               f'Wind is blowing at {round(response["wind"]["speed"] * 3.6, 2)}km/h\n' \
               f'Visibility is {int(response["visibility"] / 1000)}km'
        return weather
    except requests.exceptions.RequestException:
        return None
    except KeyboardInterrupt:
        return None

def get_general_response(query):
    if not Client or not WOLFRAMALPHA:
        return None
    try:
        client = Client(app_id=WOLFRAMALPHA)
        response = client.query(query)
        return next(response.results).text
    except (StopIteration, AttributeError) as e:
        return None
    except KeyboardInterrupt:
        return None
    except Exception:
        return None

def get_popular_movies():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/movie/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for movie in response["results"]:
            title = movie['title']
            print(title)
    except KeyError:
        return None

def get_popular_tvseries():
    try:
        response = requests.get(f"https://api.themoviedb.org/3/tv/popular?api_key={TMDB}&region=IN&sort_by=popularity.desc&"
                                f"primary_release_year={datetime.date.today().year}").json()
    except requests.exceptions.RequestException:
        return None
    try:
        print()
        for show in response["results"]:
            title = show['name']
            print(title)
    except KeyError:
        return None