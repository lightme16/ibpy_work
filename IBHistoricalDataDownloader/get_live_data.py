from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
from ib.ext.TickType import TickType as tt
import time, sys
import pandas as pd

def convert_date(old_date):
    new_date = ''.join(old_date.split('-')[::-1])
    return new_date

symbol = sys.argv[1]
exch = sys.argv[2]
expiry = convert_date(sys.argv[3])
delay = int(sys.argv[4])
#better to read these from a file
contracts = pd.DataFrame([
        [symbol,exch,'USD',expiry]
])

# make decent column names
contracts.columns = ['sym','exch','curr','expiry']

#add these specific column names to match the name returned by TickType.getField()
contracts['bidPrice'] = 0
contracts['askPrice'] = 0
contracts['lastPrice'] = 0


# def error_handler(msg):
#     print (msg)

def my_callback_handler(msg):
    if msg.field in [tt.BID, tt.ASK, tt.LAST]:
        # now w e can just store the response in the data frame
        contracts.loc[msg.tickerId, tt.getField(msg.field)] = msg.price
        # if msg.field == tt.LAST:
        #     print(contracts.loc[msg.tickerId, 'sym'], msg.price)

tws = ibConnection(port=7496, clientId=996)
tws.register(my_callback_handler, message.tickPrice, message.tickSize)
# tws.register(error_handler, 'Error')
tws.connect()

while True:
    for index, row in contracts.iterrows():
        c = Contract()
        c.m_symbol = row['sym']
        c.m_exchange = row['exch']
        c.m_currency = row['curr']
        c.m_secType ='FUT'
        c.m_expiry = row['expiry']
        # the tickerId is just the index in but for some reason it needs str()
        tws.reqMktData(str(index),c,"",False)
    time.sleep(delay)
    print("%s %s %s: %s" %(contracts.loc[0, 'sym'], contracts.loc[0, 'exch'], contracts.loc[0, 'expiry'],
                                     contracts.loc[0, 'lastPrice']))
    if delay == 1:
        time.sleep(1)
    else:
        time.sleep(delay-1)
    CURSOR_UP_ONE = '\x1b[1A'
    ERASE_LINE = '\x1b[2K'
    print CURSOR_UP_ONE + ERASE_LINE + CURSOR_UP_ONE


time.sleep(3)
tws.close()
