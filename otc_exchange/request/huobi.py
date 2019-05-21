from base import BaseExchange

class Huobi(BaseExchange):

    def __init__(self,debug = False):
        BaseExchange.__init__(self,debug=debug)
        self.exchange = 'huobi'
        self.url = 'https://otc-api.eiijo.cn/v1/data/trade-market?' \
                   'country=37&currency=1&payMethod=0&currPage=1&coinId=5&' \
                   'tradeType={}&blockType=general&online=1'

    def phase_price(self):
        data = {}
        for side in self.sides:
            data[side] = self.trade_market[side].json()['data']

        # print(data['buy'])
        # exit()
        self.price = {
            'exchange': self.exchange,
            'price': {
                'bid': float( data['buy'][0]['price'] ),
                'ask': float( data['sell'][0]['price'] )
            }

        }

if __name__ == '__main__':
    huobi = Huobi(debug=True)

    huobi.test()
