# This is a sample Python script.
import requests
import json
import hashlib
import itertools
# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

BASEURL = 'https://optiondata-beta.aliceblueonline.com/'

def Optionchainlogin(user_id,session_id):

    #print(f'Hi, {user_id,session_id}')
    url = BASEURL + 'api/UsersAuth/login';
    payload = json.dumps({
        "clientCode": user_id,
        "token": session_id
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    print(response.text)
    token = response.text




    global Token
    Token=token
    #print(token[71:692])
    #Token=token


def PremiumDashboard():
    url = BASEURL + 'api/v1/PremiumDashboard';
    payload = json.dumps({


    })
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)

def CardsMargin(code,segment,name,expiry,strike,ltp,quantity,code1,segment1,name1,expiry1,strike1,ltp1,quantity1,code2,segment2,name2,expiry2,strike2,ltp2,quantity2,code3,segment3,name3,expiry3,strike3,ltp3,quantity3,spot_price,exchange):
    url = BASEURL + 'api/v1/CardsMargin';
    payload = json.dumps({
        "first_card": [
            {
                "code": code,
                "segment": segment,
                "name": name,
                "expiry": expiry,
                "strike": strike,
                "ltp": ltp,
                "quantity": quantity
            },
            {
                "code": code1,
                "segment": segment1,
                "name": name1,
                "expiry": expiry1,
                "strike": strike1,
                "ltp": ltp1,
                "quantity": quantity1
            }
        ],
        "second_card": [
            {
                "code": code2,
                "segment": segment2,
                "name": name2,
                "expiry": expiry2,
                "strike": strike2,
                "ltp": ltp2,
                "quantity": quantity2
            },
            {
                "code": code2,
                "segment": segment2,
                "name": name2,
                "expiry": expiry2,
                "strike": strike2,
                "ltp": ltp2,
                "quantity": quantity2
            }
        ],
        "third_card": [
            {
                "code": code3,
                "segment": segment3,
                "name": name3,
                "expiry": expiry3,
                "strike": strike3,
                "ltp": ltp3,
                "quantity": quantity3
            },
            {
                "code": code3,
                "segment": segment3,
                "name": name3,
                "expiry": expiry3,
                "strike": strike3,
                "ltp": ltp3,
                "quantity": quantity3
            }
        ],
        "spot_price": spot_price,
        "exchange": exchange
    })
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def Getlix(exchange,quantity,segment,strike,code,op_pr,name,expiry):
    url = BASEURL + 'api/v1/GetLIX';
    payload = json.dumps({
      "exchange": exchange,
      "quantity": quantity,
      "segment":segment,
      "strike": strike,
      "code":code,
      "op_pr": op_pr,
      "name": name,
      "expiry": expiry
    } )
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def GetMarginBasedOption(tab_name,name,expiry,spot_price,code,exchange):
    url = BASEURL + 'api/v1/GetMarginBasedOption';
    payload = json.dumps({
    "tab_name": tab_name,
    "name": name,
    "expiry": expiry,
    "spot_price": spot_price,
    "code": code,
    "exchange":exchange

})
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def MoreCards(tab_name,name,expiry,spot_price,exchange):
    url = BASEURL + 'api/MoreCrads1/MoreCrads';
    payload = json.dumps({
  "tab_name":tab_name,
  "name": name,
  "expiry": expiry,
  "spot_price": spot_price,
  "exchange": exchange
})
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def OpenInterest(date,cm,cm_1,cm_2,short,long):
    url = BASEURL + 'api/v1/OpenInterest';
    payload = json.dumps(
{
  "date": date,
  "cm": bool(cm),
  "cm_1": bool(cm_1),
  "cm_2": bool(cm_2),
  "short": short,
  "long": long
} )
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def optionGreeks(strike_price,spot_price,price,days_to_expire):
    url = BASEURL + 'api/v1/OptionGreeks';
    payload = json.dumps({

  "strike_price": strike_price,
  "spot_price":spot_price,
  "price": price,
  "days_to_expire": days_to_expire
})
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def OptionSpan(expiry,name,strike,segment,quantity,op_pr,code,trading_symbol):
    url = BASEURL + 'api/v1/OptionSpan';
    payload = json.dumps({
    "expiry": expiry,
      "name": name,
      "strike": strike,
      "segment": segment,
      "quantity": quantity,
      "op_pr": op_pr,
      "code": code,
      "trading_symbol": trading_symbol
})
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def OptionStrategy(tab,combo,expiry,ltp,name,days_to_expire,target_days,exchange):
    url = BASEURL + 'api/v1/Optionstrategy';
    payload = json.dumps({
   "tab": tab,
  "combo": combo,
  "expiry": expiry,
  "ltp": ltp,
  "name":name,
  "days_to_expire": days_to_expire,
  "target_days": target_days,
  "exchange": exchange
})
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)


def StrategyBuilder(expiry,quantity,op_type,strike,tr_type,op_pr,trading_symbol,spot_price,code,exchange,days_to_expire,target_days):
    url = BASEURL + 'api/v1/StrategyBuilder';
    payload = json.dumps({
  "expiry": expiry,
      "quantity": quantity,
      "op_type": op_type,
      "strike": strike,
      "tr_type": tr_type,
      "op_pr": op_pr,
      "trading_symbol": trading_symbol,
 "spot_price": spot_price,
  "user_id": "",
  "code": code,
  "exchange": exchange,
  "days_to_expire": days_to_expire,
  "target_days": target_days
})
    headers = {'Content-Type': 'application/json',
               "Authorization": "Bearer " + Token[71:692]
               }
    response = requests.request("POST", url, headers=headers, data=payload)
    # print("GET Option greeks	 ",response.text)
    testing = response.text
    # print(testing)
    print(testing)