from flask import Flask
import time
from datetime import datetime
from datetime import datetime
from binance.client import Client
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
# declare the bianance client 
client = Client("", "")
output=[]

#Question 2
# top 5 symbols with quote asset BTC and the highest volume over the last 24 hours in descending order
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

#Question 4
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

#Question 5
def interval_data():
    prev_data={}
    current_data={}
    top_symbol=get_usdt_data("USDT",5)
    while(True):
        prev_data=spread_data(top_symbol)
        time.sleep(10)
        current_data=spread_data(top_symbol)
        i=0
        info = {}
        while i in range(5):
            info['symbol']=prev_data[i]["symbol"]
            info['spread_value']=str(abs(float(prev_data[i]["spread_value"])-float(current_data[i]["spread_value"])))
            output.append(info)
            info = {}
            i=i+1
            if len(output)>5:
                output.pop(0)
        #print(output)
        top_symbol=get_usdt_data("USDT",5)
        
# To run interval_data in background
background_query = BackgroundScheduler(daemon=True)
background_query.add_job(interval_data,'interval',seconds=10.01)
background_query.start()

#Question 6
@app.route('/metrics', methods=['GET'])
def metrics():
    temp_data="<meta http-equiv=\"refresh\" content=\"10\" >"+"# Delta of price spread of top 5 symbol of highest number of trades with asset USDT on time <l style=\"color:blue;\">"+str(datetime.now())+"<br><d style=\"color:black;\">"
    if len(output)>1:
         for data in output:
            temp_data=temp_data+"{symbol="+data['symbol']+", "+"spread_value="+data['spread_value']+ "}\n"+"<br>"
         return temp_data
    else:    
         return "<meta http-equiv=\"refresh\" content=\"10\" ><style>h1 {text-align: center;}p {text-align: center;}div {text-align: center;}</style><h1>Wait 10 sec to fetch Data first time.....<h1> "
@app.route("/", methods=['GET'])
def index():
    return "<style>h1 {text-align: center;}p {text-align: center;}div {text-align: center;}</style><h1>Hello Bianace !!!!!! </h1><pr><h1>Click to see :<a href='metrics'> Price Spread Data Delta Metrics</a> <h1>"

if __name__ == '__main__':
    app.run(host='localhost', port=8080)
