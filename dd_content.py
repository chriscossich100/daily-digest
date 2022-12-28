import random
import requests
from urllib import request #the request module from the urllib package which allows us to open the url for the api
import json #this will parse the response
import datetime #this module will format will save the timestamps for all the periods.
import tweepy
"""
Retrieve a random quote from the specified CSV file.
"""
def get_random_quote(quotes_file='quotes.csv'):
    try:
        f = open('quotes.json')
        # returns JSON object as a dictionary
        data = json.load(f)
        eachData = data['personalQuotes']
        randomQuote = random.choice(eachData)
    except Exception as e:
        randomQuote = {
            "quote": "this is a default quote because there was an error loading the personal quotes",
            "author": "admin"
        }
    return randomQuote

 
"""
Retreive weather forcast based of geographical location.
"""
def get_weather_forecast(): #here we are going to use our own version of a get request. 38.901011, -77.015690

    #Remember when trying to receive or send information from the internet, it's always best to use a try block
    try:
        apiKey = '48ef76dd06c684c6abd02d37d95a18b1'
        lat = 38.901011
        long = -77.015690
        url = f'http://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={long}&appid={apiKey}&units=imperial'
        x = requests.get(url)
        print(x)
        data = x.json() #once we get the request, we are simply assigning data to the json parsed information
        lists = [] #contains the list of all temps throughout the days for 5 days. In our case we are only getting 36 hour weather.
        forecast = { #create a dictionary that is going to contain all our weather information, we will print this out.
            "city": data["city"]["name"], #contain the name of the city we are in
            "country": data["city"]["country"],
            "lists": lists
        } 
        for coolio in data["list"][0:9]:
            lists.append({
                "timestamp": datetime.datetime.fromtimestamp(coolio["dt"]),
                "temp": round(coolio["main"]["temp"]),
                "description": coolio["weather"][0]["description"],
                "icon": f'http://openweathermap.org/img/wn/{coolio["weather"][0]["icon"]}.png'}
            )

        return forecast

    except Exception as e:
        print(e)
    pass

def get_twitter_trends(woeid=23424977):
    
    #remember that if you're retrieving information from the internet, there could be some issues even if you didnt code anything wrong. 
    #that's why try catch blocks are around.
    try: # retrieve Twitter trends for specified location
        api_key = '0wotJJpm0GnOjiSaxpBkRfiN7' # replace with your own Twitter API key
        api_secret_key = 'HO5aabRoZSZIaGIm6NfNDf0OIhjoMELMswvmHFCox52nKW780o' # replace with your own Twitter API secret key
        auth = tweepy.AppAuthHandler(api_key, api_secret_key)
        return tweepy.API(auth).get_place_trends(woeid)[0]['trends'] # NOTE: Tweepy 4.0.0 renamed the 'trends_place' method to 'get_place_trends'

    except Exception as e:
        print(e)
"""
Retrieve the summary extract for a random Wikipedia article.
"""
def get_wikipedia_article():
    
    #to get wikipedia random article we are going to use the requests package to make a get request.
    #again, remember that if you're retrieving information from the internet, there culd be some issues even if hyou didnt code anything wrong.
    #this is where the try catch block comes in handy:
    try:
        url = "https://en.wikipedia.org/api/rest_v1/page/random/summary" #url used in request.

        x = requests.get(url) #the get method is being used from the requests package. it will return information in data format. set x = equal to the data returned.
        data = x.json() #once the data has been returned, convert it to json

        #return a dictionary
        return {"title": data["title"], "extract": data["extract"], "url": data["content_urls"]["desktop"]["page"]}

    except Exception as e:
        print(e)
        
if __name__ == '__main__':
    ##### test get_random_quote() #####
    print('\nTesting quote generation...')

    quote = get_random_quote()
    print(f' - Random quote is "{quote["quote"]}" - {quote["author"]}')

    quote = get_random_quote(quotes_file = None)
    print(f' - Default quote is "{quote["quote"]}" - {quote["author"]}')

    ##### test get_weather_forecast() #####
    print('\nTesting weather forecast retrieval...')

    forecast = get_weather_forecast() # get forecast for default location
    if forecast:
        print(f'\nWeather forecast for {forecast["city"]}, {forecast["country"]} is...')
        for period in forecast['lists']:
            print(f' - {period["timestamp"]} | {period["temp"]}°C | {period["description"]}')

    ##### test get_twitter_trends() #####
    print('\nTesting Twitter trends retrieval...')

    trends = get_twitter_trends() # get trends for default location of United States
    if trends:
        print('\nTop 10 Twitter trends in the United States are...')
        for trend in trends[0:10]: # show top ten
            print(f' - {trend["name"]}: {trend["url"]}')

    trends = get_twitter_trends(woeid = 44418) # get trends for London
    if trends:
        print('\nTop 10 Twitter trends in London are...')
        for trend in trends[0:10]: # show top ten
            print(f' - {trend["name"]}: {trend["url"]}')

    trends = get_twitter_trends(woeid = -1) # invalid WOEID
    if trends is None:
        print('Twitter trends for invalid WOEID returned None')

    ##### test get_wikipedia_article() #####
    print('\nTesting random Wikipedia article retrieval...')

    article = get_wikipedia_article()
    if article:
        print(f'\n{article["title"]}\n<{article["url"]}>\n{article["extract"]}')