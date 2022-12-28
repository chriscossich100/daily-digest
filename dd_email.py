import dd_content
import datetime
import smtplib
from email.message import EmailMessage

class DailyDigestEmail:

    def __init__(self):
        self.content = {
            "quote": {"include": True, "content": dd_content.get_random_quote()},
            "weather": {"include": True, "content": dd_content.get_weather_forecast()},
            "twitter": {"include": True, "content": dd_content.get_twitter_trends()},
            "wikipedia": {"include": True, "content": dd_content.get_wikipedia_article()}
        }
        #instance variable of the dailydigest email class.
        self.recipients = []
        #instance variables of the dailydigestemail class
        self.sender_credentials = {}
        

    def send_email(self):
        print("Sending Emails to Recipient(s)...")

        coolioMessage = self.format_message()
        #set msg equal to the EmailMessage class.
        for rec in self.recipients:
            msg = EmailMessage()
            msg.set_content(coolioMessage['text']) 
            # #if adding an html message, we will need to add the add.alternative module.
            msg.add_alternative(coolioMessage["html"], subtype = "html")
            msg['Subject'] = 'Daily Digest'
            msg['From'] = self.sender_credentials['email']
            msg['To'] = [rec]
            with smtplib.SMTP('smtp.office365.com', 587) as smtp:
                #the starttls object puts the smtp connection in TLS (Transport Layer Security) mode. All the SMTP comamnds that follow will be encrypted.
                smtp.starttls()
                smtp.login(self.sender_credentials['email'], self.sender_credentials['password'])
                smtp.send_message(msg)

        print("Emails has been sent!")

    def format_message(self):
        #THIS PART GENERATES PLAIN TEXT DOCUMENT.
        text = f"{datetime.date.today().strftime('%d %b %Y')} \n\n"
        
        #add the random quote into our plain text document.
        quote = self.content["quote"]["content"]
        text += f"--- OUR QUOTE OF THE DAY --- \n\n"
        text += f'\"{self.content["quote"]["content"]["quote"]} - {self.content["quote"]["content"]["author"]}\"\n\n'
        
        #add forecast information to our plain text document.
        forecastInfo = self.content["weather"]["content"]
        text += f"--- Forecast for {forecastInfo['city']}, {forecastInfo['country']} --- \n\n"
        for weatherinfos in forecastInfo["lists"]:
            text += f"{weatherinfos['timestamp'].strftime('%d %b %H%M')} | {weatherinfos['temp']}°F | {weatherinfos['description']}\n"

        # get trending twitter topics and put them onto the text file.
        text += "\n--- Top 10 Twitter Trends Right Now ---\n\n"
        twitterInfo = self.content["twitter"]["content"]
        for eachTwitterInfo in twitterInfo[0:9]: #we are only getting the first 10 of the list of trending tweets.
            text += f"{eachTwitterInfo['name']} - {eachTwitterInfo['url']}\n"

        #get random wikipedia article and put them onto the text file.
        text += "\n--- Learn Something New - Your Random Wikipedia Page ---\n\n"
        wikipediaInfo = self.content["wikipedia"]["content"]
        text += f'{wikipediaInfo["title"]} - {wikipediaInfo["extract"]} || link to page: {wikipediaInfo["url"]}'
        f = open("message_text.txt", "w+", encoding='utf-8')
        f.write(text)
        f.close()

        #THIS PART GENERATS THE HTML DOCUMENT:

        html = f"""<html>
            <head>
            <title>Your Daily Digest</title>
            </head>
            <body>
            <center>
            <h1>Your Daily Digest - {datetime.date.today().strftime('%d %b %Y')}</h1>
            <h2> Quote of the Day</h2>
            <i>"{quote['quote']}"</i> - {quote['author']}
            <h2> Forecast for {forecastInfo['city']}, {forecastInfo["country"]} </h2>
            <table>
        """
        #get the weather information and then put it into the html document: forecastInfo['lists']
        for eachInfo in forecastInfo['lists']: 
            html += f"""
                <tr>
                <td> {eachInfo['timestamp'].strftime('%d %b %H%M')} |</td>
                <td> {eachInfo['temp']}°F |</td>
                <td> {eachInfo['description']} </td>
                <td><img src = "{eachInfo['icon']}" /></td>
                </tr>
                
            """
        html += """
            </table>
            <h2> Top 10 Twitter Trends</h2>
            """
        #get the twitter infromation and then put it into the html document: twitterInfo
        for listTwitters in twitterInfo[0:9]:
            html += f"""
                <p><a href = "{listTwitters['url']}">{listTwitters['name']}</a></p>
            """
        #format wikipedia information and then put in into the html document: wikipediaInfo[]
        html += f"""
            <h2>Daily Random Knowledge</h2>
            <h3><a href = "{wikipediaInfo['url']}">{wikipediaInfo['title']}</a></h3>
            <table width="800">
            <tr>
                <td>{wikipediaInfo['extract']}</td>
            </tr>
            </table>
        """
        #end of html document
        html += """
            <p>Unsubscribe <a href="#">here</a></p>
            </center>
            </body>
            </html>
        """
        # print(html)
        sendToHtml = open("message_html.html", "w", encoding='utf-8')
        sendToHtml.write(html)
        sendToHtml.close()

        return {
            "text": text,
            "html": html
        }
        

if __name__ == '__main__':
    #set content equal to DailyDigestEmail class. 
    content = DailyDigestEmail()
    finalMessage = content.format_message()
    content.send_email()