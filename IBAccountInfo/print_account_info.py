from time import sleep
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message

def my_account_handler(msg):
    print(msg)


def my_tick_handler(msg):
    print(msg)


if __name__ == '__main__':
    con = ibConnection(port=7496, clientId=996)
    con.register(my_account_handler, 'UpdateAccountValue')
    con.connect()

    def inner():

        con.reqAccountUpdates(1, '')

    inner()
    sleep(5)
    print('disconnected', con.disconnect())
    inner()
    sleep(3)
