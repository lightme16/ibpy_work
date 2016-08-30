#! /usr/bin/env python
# -*- coding: utf-8 -*-

from ib.ext.Contract import Contract
from ib.ext.Order import Order
from ib.opt import ibConnection, message
from time import sleep, time

# print all messages from TWS
def watcher(msg):
    print msg

# show Bid and Ask quotes
def my_BidAsk(msg):
    if msg.field == 1:
        print '%s:%s: bid: %s' % (contractTuple[0],
                       contractTuple[6], msg.price)
    elif msg.field == 2:
        print '%s:%s: ask: %s' % (contractTuple[0], contractTuple[6], msg.price)

def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    #newContract.m_strike = contractTuple[5]
    #newContract.m_right = contractTuple[6]
    print '\nContract Values:%s,%s,%s,%s,%s,%s,%s:' % contractTuple
    return newContract

def makeFutOrder(type, action, orderId=-99, price=None):
    order = Order()
    order.m_orderId = orderId
    order.m_clientId = 0
    order.m_permid = 0
    order.m_orderType = type
    order.m_action = action
    order.m_minQty = 1
    order.m_totalQuantity = 1
    # order.m_transmit = False
    if type == 'LMT':
        order.m_lmtPrice = price
    if action == 'SELL':
        pass

    return order

if __name__ == '__main__':
    con = ibConnection(port=7496, clientId=991)
    con.registerAll(watcher)
    showBidAskOnly = True  # set False to see the raw messages
    if showBidAskOnly:
        con.unregister(watcher, message.tickSize, message.tickPrice,
                       message.tickString, message.tickOptionComputation)
        con.register(my_BidAsk, message.tickPrice)

    do_sell = False

    while True:
        con.connect()
        oid = int(time())
        sleep(1)
        tickId = 1

        # Note: Option quotes will give an error if they aren't shown in TWS
        #contractTuple = ('QQQQ', 'STK', 'SMART', 'USD', '', 0.0, '')
        #contractTuple = ('QQQQ', 'OPT', 'SMART', 'USD', '201609', 47.0, 'CALL')
        contractTuple = ('ES', 'FUT', 'GLOBEX', 'USD', '201609', 0.0, '')
        #contractTuple = ('M6E', 'FUT', 'GLOBEX', 'EUR', '20160919')#, 0.0, '')
        #contractTuple = ('ES', 'FOP', 'GLOBEX', 'USD', '20070920', 1460.0, 'CALL')
        #contractTuple = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')

        futContract = makeStkContract(contractTuple)
        print '* * * * REQUESTING MARKET DATA * * * *'
        con.reqMktData(tickId, futContract, '', False)
        sleep(5)
        print '* * * * CANCELING MARKET DATA * * * *\n* * * * PROCESSING ORDER * * * *'
        con.cancelMktData(tickId)
        sleep(2)

        if do_sell:
            action = 'SELL'
        else:
            action = 'BUY'

        futOrder = makeFutOrder('MKT', action)
        sleep(2)
        con.placeOrder(oid, futContract, futOrder)
        sleep(5)
        do_sell = not do_sell
        print 'Order is placed!'
        con.disconnect()
        sleep(4)
