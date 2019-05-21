from base import BaseExchange
import pandas as pd
import time

class Okex(BaseExchange):

    def __init__(self,baseCurrency = 'eos',paymentMethod = 'all',debug = False):
        BaseExchange.__init__(self,debug=debug)
        self.exchange = 'okex'
        self.url = 'https://www.okex.me/v3/c2c/tradingOrders/' \
                   'book?side={}'+ \
                  '&baseCurrency={}'.format(baseCurrency)+ \
                  '&quoteCurrency=cny&userType=all' +\
                  '&paymentMethod={}'.format(paymentMethod)

        self.df = {}

    def get_trademarket(self):
        for side in self.sides:
            self.trade_market[side] = self.session.get( self.url.format( side ) )

    def phase_price(self):
        data = {}
        self.df = {}
        for side in self.sides:
            data[side] = self.trade_market[side].json()['data']
            #print(data[side][side])
            self.df[side] = pd.DataFrame(data[side][side],
                columns=['price','quoteMinAmountPerOrder'])

        self.price = {
            'exchange': self.exchange,
            'price': {
                'bid': float( data['buy']['buy'][0]['price'] ),
                'ask': float( data['sell']['sell'][0]['price'] )
            }

        }

if __name__ == '__main__':
    okex = Okex(baseCurrency = 'usdt',paymentMethod='aliPay')
    equ = 0
    sma =0
    while True:
        try:
            okex.get_trademarket()
            okex.phase_price()

            buy_df = okex.df['buy']

            buy400_df = buy_df[buy_df.quoteMinAmountPerOrder < 1000]

            sell_df = okex.df['sell']

            #print(sell_df.sort_index(axis=0, by=None, ascending=False) .tail())
            #print(buy_df.head())

            sell400_df = sell_df[sell_df.quoteMinAmountPerOrder <1000]


            print(sell400_df.sort_index(axis=0, by=None, ascending=False) .tail())

            print( buy400_df.head() )
            buy = buy400_df.iat[0,0]
            sell = sell400_df.iat[0,0]

            print('buy={},sell={}'.format(buy,sell),'buy=sell', equ,'sell < buy:', sma)

            if sell ==buy:
                equ += 1
            elif sell < buy:
                sma += 1
        except:
            pass
        time.sleep(1)





