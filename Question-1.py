from itertools import count
import time
from datetime import datetime
from binance.client import Client
# declare the bianance client 
client = Client("", "")

# Function top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order
def get_btc_data(asset,num):
    sorted_data=sorted(client.get_ticker(), key = lambda i: float(i['volume']))
    result=[] 
    count=0
    while sorted_data and count!=num:
        data=sorted_data.pop(-1)
        res  = {key:val for key, val in data.items() if key in "symbol" and val.endswith(asset)} 
        if res != {}:
          result.append(data["symbol"]+":"+data["volume"])
          count=count+1
        res={}
    return result

if __name__ == "__main__":
    btc_data=get_btc_data("BTC",5)
    print("Top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order")
    for data in btc_data:
       print(data)