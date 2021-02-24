# Do `pip install nsetools`, documentation at https://nsetools.readthedocs.io/en/latest/
from nsetools import Nse
import time
import json

t = time.localtime()
current_time = time.strftime("%H:%M:%S", t)
print(current_time)

def get_qoute_tester(stock):
    stockTester = {
        'TATAMOTORS': {
            'buyPrice1': 320,
            'averagePrice': 318,
            'lastPrice': 319
        },
        'TATASTEEL': {
            'buyPrice1': 720,
            'averagePrice': 718,
            'lastPrice': 719
        }
    }

    return stockTester[stock]

# This function is on while loop with a time out of 2 seconds.
def monitor_realtime(your_stock_codes, price_level, avg_level, counter={}, prev_avg={}):
    data_packet = {}
    for stock in your_stock_codes:
        data_packet[stock] = {}

        q = nse.get_quote(stock)
        #q = get_qoute_tester(stock)

        price = q['buyPrice1']
        avg = q['averagePrice']
        last_price = q['lastPrice']

        if ((price >= price_level[stock]) and (last_price < price_level[stock])):
            price_msg = trigger_price(stock, price)
            data_packet[stock]['price_msg'] = price_msg

        if ((price >= price_level[stock] - price_level[stock] % 0.1) and (last_price < price_level[stock] - price_level[stock] % 0.1)):
            counter = trigger_count(stock, counter)
            data_packet[stock]['counter'] = counter

        if (avg >= avg_level[stock]):
            prev_avg, avg_msg = trigger_avg(stock, avg, prev_avg)
            data_packet[stock]['prev_avg'] = prev_avg[stock]
            data_packet[stock]['avg_msg'] = avg_msg

        prev_avg[stock] = avg

    return data_packet

# This function triggers a response when avg value crosses set level.
def trigger_avg(stock, avg, prev_avg):
    msg = ''
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t) 
    if stock not in prev_avg:
        prev_avg[stock] = avg
        msg = f'{stock} has hit the average level set {avg_level[stock]}'
        print(f'{stock} has hit the average level set {avg_level[stock]} at {current_time}')
    elif (avg > avg_level[stock] > prev_avg[stock]):
        msg = f'{stock} has hit the average level set {avg_level[stock]}'
        print(f'{stock} has hit the average level set {avg_level[stock]} at {current_time}')

    return prev_avg, msg

# This function triggers a response when current price crosses set level.
def trigger_price(stock, price):
    t = time.localtime()
    current_time = time.strftime("%H:%M:%S", t)
    msg = f'{stock} has hit the price level set {price}'
    print(f'{stock} has hit the price level set {price} at {current_time}')
    return msg

# This function counts the number of times the stock hits +-0.1% of our level.
def trigger_count(stock, counter):
    if stock not in counter:
        counter[stock] = 1
    else:
        counter[stock] += 1

    return counter

# Creates the json data packet for front-end.
def set_datapacket(datapacket):
    json.dump(datapacket, open("datapacket.json", "w"))


nse = Nse()

#Add your stock codes here (NSE CODES)
your_stock_codes = ['TATAMOTORS', 'TATASTEEL']

# Set your price and avg levels below
price_level = {
    'TATAMOTORS': 326,
    'TATASTEEL': 730
}

avg_level = {
    'TATAMOTORS': 325,
    'TATASTEEL': 725
}

counter = {}
prev_avg = {}

while True:
    datapacket = monitor_realtime(your_stock_codes, price_level, avg_level, counter, prev_avg)
    time.sleep(2)
    set_datapacket(datapacket)
