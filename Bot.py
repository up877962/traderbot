import time
import cbpro
data = open('keys.txt', 'r').read().splitlines()
public = data[0]
passphrase = data[1]
secret = data[2]
public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(public, secret, passphrase)


class Bot:
    def __init__(self, sp, sa, bp, ba, currency):
        self.sell_price = sp
        self.sell_amt = sa
        self.buy_price = bp
        self.buy_amt = ba
        self.currency = currency



    # sell_price = 0.3300
    # sell_amt = 38.0
    #
    # buy_price = 0.3000
    # buy_amt = 38.0
    #currency = 'XLM-EUR'

    def launcher(self):

        safety_price = (self.buy_price/3)*2

        print 'sell at:', self.sell_price, 'buy at:', self.buy_price, 'safety price:', safety_price
        while True:

            price = float(auth_client.get_product_ticker(product_id=self.currency)['price'])
            print 'current price:', price
            if price <= self.buy_price and price > safety_price:
                print('buying XLM for')
                auth_client.buy(size=self.buy_amt, order_type='market', product_id=self.currency)
            elif price >= self.sell_price:
                auth_client.sell(size=self.sell_amt, order_type='market',product_id=self.currency)
                print('selling XLM')
            else:
                print('no orders placed')
            time.sleep(30)

# 'XLM-EUR'
#####################################################################################################################
# bot = Bot(0.3300, 38.0, 0.3000, 38.0,'XLM-EUR')
# bot.launcher()