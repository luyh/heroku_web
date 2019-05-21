from requests_html import HTMLSession
import json


class BaseExchange():
    def __init__(self,debug = False):

        self.session = HTMLSession()

        # okex example
        self.url = 'https://www.okex.me/v3/c2c/tradingOrders/book?' \
                  'side={}&baseCurrency=eos&quoteCurrency=cny' \
                  '&userType=all&paymentMethod=all'
        self.exchange = 'base'

        self.sides = ['buy','sell']
        self.trade_market = {}
        self.price = {}

        self.debug = debug


    def get_trademarket(self):
        for side in self.sides:
            self.trade_market[side] = self.session.get( self.url.format( side ) )
        
    def phase_price(self):
        data = {}
        for side in self.sides:
            data[side] = self.trade_market[side].json()['data']

        self.price = {
            'exchange': self.exchange,
            'price': {
                'buy': float( data['buy']['buy'][0]['price'] ),
                'sell': float( data['sell']['sell'][0]['price'] )
            }

        }

    def print_json_data(self,data):
        print( json.dumps( data, indent=2 ) ,end='\r')

    def get_price(self):
        self.get_trademarket()
        self.phase_price()

    def test(self):
        self.get_price()

        if self.debug:
            for side in self.sides:
                print(self.trade_market[side].json())

        self.print_json_data(self.price)

if __name__ == '__main__':

    base = BaseExchange(debug=True)

    base.test()

