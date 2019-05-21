from base import BaseExchange

class Coinmydex(BaseExchange):

    def __init__(self,debug = False):
        BaseExchange.__init__(self,debug=debug)
        self.exchange = 'coinmydex'
        self.url = 'https://api.coinmydex.com/otc/27'

    def get_trademarket(self):
        self.trade_market = self.session.get( self.url )

    def phase_price(self):
        data= self.trade_market.json()['data']

        self.price = {
            'exchange': self.exchange,
            'price': {
                'ask': round(float( data['buyPrice'] )*1.002*1.0015,2),
                'bid': round(float( data['sellPrice'] )/1.002/1.0015,2)
            }
        }

    def test(self):
        self.get_price()

        if self.debug:
            for side in self.sides:
                print( self.trade_market.json() )

        self.print_json_data( self.price )

if __name__ == '__main__':
    coinmydex = Coinmydex(debug=True)

    coinmydex.test()