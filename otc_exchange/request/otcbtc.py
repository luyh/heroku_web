from base import BaseExchange


class Otcbtc(BaseExchange):

    def __init__(self,debug = False):
        BaseExchange.__init__(self,debug=debug)
        self.exchange = 'otcbtc'
        self.url = 'https://otcbtc.com/{}_offers?currency=eos&fiat_currency=cny&payment_type=all'

    def get_price(self):
        data = {}
        for side in self.sides:
            response = self.session.get(self.url.format(side))
            data[side] = float(response.html.find('div.recommend-card__price',first = True).text)

        self.price = {
            'exchange': self.exchange,
            'price': {
                'bid': round(float( data['buy']),2),
                'ask': round(float( data['sell'] ),2)
            }

        }


if __name__ == '__main__':
    otcbtc = Otcbtc(debug=True)

    otcbtc.get_price()
    otcbtc.print_json_data(otcbtc.price)