from itertools import count
import time
from datetime import datetime
from binance.client import Client
# declare the bianance client 
client = Client("", "")
def get_usdt_data(asset,num):
    client_data=client.get_ticker()
    count=0
    info = {}
    result=[] 
    trade_data=[]
    while client_data:
        temp_data=client_data.pop(-1)
        res  = {key:val for key, val in temp_data.items() if key in "symbol" and val.endswith(asset)} 
        if res != {}:
           trade=float(temp_data["bidQty"])+float(temp_data["askQty"])
           info['symbol']=temp_data["symbol"]
           info["trade_value"]=str(trade)
           trade_data.append(info)
        res={}
        info = {}
    sorted_data=sorted(trade_data, key = lambda i: float(i['trade_value']))
    while sorted_data and count!=num:
        data=sorted_data.pop(-1)
        result.append(data["symbol"]+" : "+data["trade_value"])
        count=count+1
    return result

#data= get_usdt_data("USDT",5)
def spread_data(data):
    top_symbol=data
    info = {}
    result=[] 
    for sym in top_symbol:
        temp_data=client.get_ticker(symbol=sym.split()[0])
        info['symbol']=temp_data["symbol"]
        info["spread_value"]=str(abs(float(temp_data["bidPrice"])-float(temp_data["askPrice"])))
        result.append(info) 
        info = {}
    return result
if __name__ == "__main__":
    usdt_spread_data=spread_data(get_usdt_data("USDT",5))
    print("Price spread for each of the symbols from Quetion: Top 5 symbols with quote asset USDT and the highest number of trades over the last 24 hours")
    for data in usdt_spread_data :
        print(data['symbol'],":",data['spread_value'] )