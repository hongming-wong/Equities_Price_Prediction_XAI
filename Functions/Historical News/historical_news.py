import requests
import os
from dotenv import load_dotenv
import json
from Functions.sp500 import sp500
from Functions.config import API_KEY

load_dotenv()

tickers = sp500.get_sp500_tickers()

for stock in tickers:
    response = requests.get(f"https://eodhistoricaldata.com/api/news?api_token={API_KEY}&s={stock}&from=2022-01-01&to=2022-10-01&offset=0&limit=1000")

    print(json.loads(response.content)[0])