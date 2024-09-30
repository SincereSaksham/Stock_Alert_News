import requests
from twilio.rest import Client

account_sid = "Your Account Sid"
auth_token = "Your auth token"

STOCK_NAME = "TSLA"  #stock name can be prompted to user, here hardcoded
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_KEY = "stock key"
STOCK_PARAMETERS = {
    "function": "TIME_SERIES_DAILY",
    "symbol": "TSLA",
    "outputsize": "compact",
    "apikey": STOCK_KEY
}
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_KEY = "news key"
NEWS_PARAMETERS = {
    "q": "tesla",
    "apikey": NEWS_KEY,
}

# ---------------------------STOCK PRICE FETCH AND PERCENTAGE CALCULATION-------------------------------#
stock_response = requests.get(url=STOCK_ENDPOINT, params=STOCK_PARAMETERS)
stock_data_list = [float(value["4. close"]) for (key, value) in stock_response.json()["Time Series (Daily)"].items()]
ystrdy_cls_price = stock_data_list[0]
day_bfr_ystr_price = stock_data_list[1]
stock_price_percent = (abs(ystrdy_cls_price - day_bfr_ystr_price) / day_bfr_ystr_price) * 100
# ----------------------------ENDS--------------------------HERE-----------------------------------------#

if stock_price_percent > 5:
    news_response = requests.get(url=NEWS_ENDPOINT, params=NEWS_PARAMETERS)
    news_data = news_response.json()
    news_data_list = []
    for i in range(3):
        news_data_list.append({news_data["articles"][i]["title"]: news_data["articles"][i]["description"]})

    client = Client(account_sid, auth_token)
    for i in range(3):
        for (key, value) in news_data_list[i].items():
            message = client.messages \
                .create(
                from_='number 1',
                body=f"Headline: {key} \n Brief:{value}",
                to='number 2'
            )

    print(message.status)

    # Optional TODO: Format the message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
