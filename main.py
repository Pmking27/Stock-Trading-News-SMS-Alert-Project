import requests
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY="Enter Your alphavantage Api Key"

NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY="Enter Your newsapi Api Key"

stock_params={
    "function":"TIME_SERIES_DAILY",
    "symbol":STOCK_NAME,
    "apikey":STOCK_API_KEY
}

response=requests.get(url=STOCK_ENDPOINT,params=stock_params)
response.raise_for_status()
data=response.json()["Time Series (Daily)"]
data_list=[value for (key,value) in data.items()]
yesterday_data=data_list[0]
yesterday_closing_price =yesterday_data['4. close']

before_yesterday_data=data_list[1]
before_yesterday_closing_price =before_yesterday_data['4. close']

differece =float(yesterday_closing_price)-float(before_yesterday_closing_price)

up_down = None
if differece > 0:
    up_down = "⬆"
else:
    up_down = "⬇"

diff_percent=round((differece/float(yesterday_closing_price))*100)
if abs(diff_percent)>5:
    news_params={
        "apiKey":NEWS_API_KEY,
        "q":COMPANY_NAME
        }
    news_response=requests.get(url=NEWS_ENDPOINT,params=news_params)
    news_response.raise_for_status()
    news_data=news_response.json()
    news_articles=news_data["articles"]
    three_news_articles=news_articles[:3]

    formatted_article=[f"{COMPANY_NAME} : {up_down}{diff_percent}%\nHeadline:{article['title']}. \nBrief:{article['description']}" for article in three_news_articles]

    account_sid = "Enter your twilio api account sid."
    auth_token =  "Enter your twilio api account auth_token."  
    my_phone_no= "Enter your twilio api verified Phone No.(Your Phone Number)"
    client = Client(account_sid, auth_token)

    for article in formatted_article:
        message = client.messages \
                        .create(
                            body=article,
                            from_="Enter your twilio api accont phone account Phone Number",
                            to=my_phone_no
                        )
        print(message.sid)               
