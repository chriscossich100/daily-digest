# daily-digest
A GUI application that can send a daily digest to any email specified using an outlook account. This is an application built using Python
and Tkinter as its GUI. The application can be opened by using running the dd-gui.py file. The application allows you the user to add/remove emails from the recipients list. The application allows the user to update the settings so that any changes are perminately set. Email sent contains different type of contents, which is set up on the dd_content.py file. The email will contain a random quote pulled from the quotes.json file. It will also contain whether information from [Open Weather Map API](http://api.openweathermap.org/). With the default coordinates being Washington D.C. (This can be changed in the dd_content.py file below the open weather api key variable) Next, the email will contain the top 10 twitter trends as of this day. Finally, there will be a link to a random wikipedia article.

_Important Notice_

Since this application uses api requests, you will need to provide your own api keys for both the [open weather map api](http://api.openweathermap.org/) and [twitter developer api keys](https://developer.twitter.com/en/docs/twitter-api). Once you have your proper api keys. You can then set them up in the proper files. for the open weather api, the api key is set on the get_weather_forecast function in the dd_content.py file. Once there, set your api key value. The same needs to be done for the twitter api. This can be set on the get_twitter_trends function found in the dd_content.py file.

```python
def get_weather_forecast(): #at the time of writing, this can be found on line 32 dd_content.py

def get_twitter_trends(): #at the time of writing, this can be found on line line 59 dd_content.py
```

Finally, in the recipients.json file, please make sure to fill out your outlook credentials. This can be skipped by simply running the application and filling out the credentials that way. Filling it out in the json file makes it permanent so that it doesnt need to be entered everytime you run the application.