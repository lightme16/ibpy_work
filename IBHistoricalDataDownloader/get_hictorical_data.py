from ib.opt import ibConnection, message
from ib.ext.Contract import Contract
import pandas as pd
import time
import sys

class Datacol:
  def error_handler(self, msg):
      print (msg)

  def __init__(self, contract, date, barsize, outfile):
    self.outfile = outfile
    self.contract = contract
    self.date = date
    #self.t = t
    self.barsize = barsize
    #self.duration = str(duration) + ' S'
    self.tick_id = 1
    self.con = ibConnection(port=7496, clientId=996)
    self.con.register(self.process_data, message.historicalData)
    #self.con.register(self.error_handler, 'Error')
    self.con.connect()
    time.sleep(1)
    end_datetime = self.date
    self.con.reqHistoricalData(tickerId=self.tick_id, contract=self.contract, endDateTime=end_datetime, durationStr='1 D', barSizeSetting=barsize, whatToShow='TRADES', useRTH=0, formatDate=1)
    self.data_received = False

  def close(self):
    while not self.data_received:
      pass
    self.con.cancelHistoricalData(self.tick_id)
    time.sleep(1)
    self.con.disconnect()
    time.sleep(1)


  def process_data(self, msg):
    if msg.open != -1:
      print "LIVE DATA: date %s, close price is %s" % (msg.date, msg.close)
      print>>self.outfile, "LIVE DATA: date %s, close price is %s" % (msg.date, msg.close)
    else:
      self.data_received = True

def convert_date(old_date):
    new_date = ''.join(old_date.split('-')[::-1])
    return new_date

def main():
  symbol = sys.argv[1]
  exch = sys.argv[2]
  expiry = convert_date(sys.argv[3])
  date = pd.to_datetime(convert_date(sys.argv[4])) - pd.DateOffset(days=1)
  to_date = pd.to_datetime(convert_date(sys.argv[5]))
  timeframe = sys.argv[6] + ' '
  units = sys.argv[7]
  duration = to_date - date

  contract = Contract()
  contract.m_symbol = symbol
  contract.m_secType = 'FUT'
  contract.m_exchange = exch
  contract.m_currency = 'USD'
  contract.m_expiry = expiry
  print 'Collecting', date, 'data for', contract.m_symbol, 'expiration', contract.m_expiry

  outfile = open('from %s to %s' % (sys.argv[4], sys.argv[5])+'.bars', 'w')

#  for h in xrange(20,24,2):
 #   broker = Datacol(contract, prev_date, ('%02d:00:00' % h), 7200, outfile)
  #  broker.close()

#  for h in xrange(0,18,2):
 #   broker = Datacol(contract, date, ('%02d:00:00' % h), 7200, outfile)
  #  broker.close()

  for h in range(duration.days):
      date = date + pd.DateOffset(days=1)
      broker = Datacol(contract, '%04d%02d%02d 21:59:00' % (date.year, date.month, date.day), timeframe+units, outfile)
      broker.close()

  outfile.close()

if __name__ == "__main__":
  main()
