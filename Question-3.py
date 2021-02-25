from itertools import count
import time
from datetime import datetime
from binance.client import Client
# declare the bianance client 
client = Client("", "")
output=[]

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

def notion_value_symbol():
    data=get_btc_data("BTC",5)
    for i in data:
        symbol_value=str(i.split(":")[0])
        notion_value=0
        temp_value=client.get_recent_trades(symbol=symbol_value,limit=200)
        for bid_data in temp_value:
            notion_value=notion_value+float(bid_data['quoteQty'])
        print(str(i.split(":")[0]),":",notion_value)

if __name__ == "__main__":
    print("Notion value of top 5 BTC Symbols ")
    notion_value_symbol()