from urllib.request import urlopen
  
import json
# from coins.models import Coin
api_key = '97345c0932caf03b68d9c0b6b74dcb79dd5462c903ccd9dfb1784081d07cd539'
def  get_coin_price(coin_symbol,currency_name='USD'):

    url =f'https://min-api.cryptocompare.com/data/price?fsym={coin_symbol}&tsyms={currency_name}&api_key={api_key}'
    response = urlopen(url)
    
    # storing the JSON response 
    # from url in data
    data_json = json.loads(response.read())
    # print the json response
    print(data_json)
    if currency_name not in data_json:
        return -1
    print(coin_symbol +": "+str(data_json['USD']))

    return data_json['USD']
   

def get_coins():
    return False
    f = open ('orders/data.json', "r")
 
    # Reading from file
    data = json.loads(f.read())
    
    for coin in data:
        Coin.add_coin(name=data[coin],symbol=coin)
        print(coin,data[coin])
    return False
