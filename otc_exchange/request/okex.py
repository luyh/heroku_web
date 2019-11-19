from base import BaseExchange
import pandas as pd
import time

class Okex(BaseExchange):

    def __init__(self,baseCurrency = 'eos',side = 'all',paymentMethod = 'all',debug = False):
        BaseExchange.__init__(self,debug=debug)
        self.exchange = 'okex'
        self.url = 'https://www.okex.me/v3/c2c/tradingOrders/' \
                   'book?side={}'.format(side)+ \
                  '&baseCurrency={}'.format(baseCurrency)+ \
                  '&quoteCurrency=cny&userType=all' +\
                  '&paymentMethod={}'.format(paymentMethod)

        self.df = {}
        self.side = side

    def get_trademarket(self):
        self.trade_market = self.session.get( self.url )
        print(self.trade_market.json())

    def phase_price(self):
        data = {}
        self.df = {}

        for side in self.sides:
            data[side] = self.trade_market.json()['data'][side]
            #print(data[side][side])
            self.df[side] = pd.DataFrame(data[side],
                columns=['price','quoteMinAmountPerOrder'])

        self.price = {
            'exchange': self.exchange,
            'price': {
                'bid': float( data['buy'][0]['price'] ),
                'ask': float( data['sell'][0]['price'] )
            }

        }

if __name__ == '__main__':
    okex = Okex(baseCurrency = 'eos')
    equ = 0
    sma =0
    while True:
        try:
            okex.get_trademarket()

            okex.phase_price()

            buy_df = okex.df['buy']

            buy400_df = buy_df[buy_df.quoteMinAmountPerOrder ==400]

            sell_df = okex.df['sell']

            #print(sell_df.sort_index(axis=0, by=None, ascending=False) .tail())
            #print(buy_df.head())

            sell400_df = sell_df[sell_df.quoteMinAmountPerOrder ==400].sort_index(axis=0, by=None, ascending=True)

            print(sell400_df.tail())
            #print(sell400_df.sort_index(axis=0, by=None, ascending=True) .tail())

            print( buy400_df.head() )

            sell400_df
        except:
            print('okex获取数据异常')
        time.sleep(3)





