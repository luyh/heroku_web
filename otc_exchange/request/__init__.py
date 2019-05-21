
from okex import Okex
from huobi import Huobi
from coinmydex import Coinmydex
from otcbtc import Otcbtc
import json,time


class OTC():
    def __init__(self,debug = False):
        self.debug = debug

        self.huobi = Huobi(debug)
        self.okex = Okex(debug)
        self.coinmydex = Coinmydex(debug)
        self.otcbtc = Otcbtc(debug)

        self.datas = {}
        self.price = {}

    def get_price(self):
        self.datas = []

        self.huobi.get_price()
        self.okex.get_price()
        self.coinmydex.get_price()
        self.otcbtc.get_price()

        self.datas.append(self.huobi.price)
        self.datas.append( self.okex.price )
        self.datas.append( self.coinmydex.price )
        self.datas.append( self.otcbtc.price )


        askPrice = {}
        bidPrice = {}
        for data in self.datas:
            askPrice[data['exchange']] = data['price']['ask']
            bidPrice[data['exchange']] = data['price']['bid']

        if self.debug:
            print(askPrice)
            print(sorted( askPrice.items(), key=lambda d: d[1], reverse= True))
            print( dict(sorted( askPrice.items(), key=lambda d: d[1], reverse=True ) ))

            print( bidPrice )
            print( sorted( bidPrice.items(), key=lambda d: d[1] ,reverse= True) )
            print( dict(sorted( bidPrice.items(), key=lambda d: d[1], reverse=True ) ))


        self.price = {}
        self.price['ask'] =dict(sorted( askPrice.items(), key=lambda d: d[1], reverse= True))
        self.price['bid'] =dict(sorted( bidPrice.items(), key=lambda d: d[1] ,reverse= True))

        if self.debug:
            print( json.dumps( self.datas, indent=2 ) )

    def print_price(self):
        print( json.dumps( self.price, indent=2 ) )


if __name__ == '__main__':
    otc = OTC()

    while True:
        otc.get_price()
        otc.print_price()
        time.sleep(3)


    # price.sort( price.items(),key=lambda item: item[1] )
    #
    # print( json.dumps( price, indent=2 ) )