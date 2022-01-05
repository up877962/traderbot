import background as background
import cbpro
import time

import configure as configure
import requests
import Tkinter as tk
import tkFileDialog as filedialog
# import ttk


data = open('keys.txt', 'r').read().splitlines()
public = data[0]
passphrase = data[1]
secret = data[2]
public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(public, secret, passphrase)

# VARIABLES
new_input = ""
text = ""
pair = {}
day = {}
book = {}
coinId ={}
singlbal ={}
x = []
labelsarray = []
splits =""
balances = []


# FUNCTION Enter a coin pairs such a algo gbp in the format 'ALGO-GBP'###############################
def statsOnSingle(coinPair):
    #print "stats on", coinPa
    global pair
    pair = public_client.get_product_ticker(product_id=coinPair)  # type: dict
    for x in pair:
        return str(x)

def formatString(ins):
    new_input = str(ins)
    lol = new_input.replace(',', '\n')
    return lol


#####FUNCTION 24 Hour stats on a currency-coin pairing
def twentyFourStats(coinpair):
    global day
    print "24 Hour Stats for", coinpair
    day = public_client.get_product_24hr_stats(product_id=coinpair)
    for x in day:
        return x,  ':', day[x]

# FUNCTION  Lists the available currency pairings, STILL NEEDS GUI INTEGRATION
def listPairs():
    list1 = public_client.get_products()
    print("A list of all coin pairs")
    for row in list1:
        print(row['id'])

# FUNCTION Get the order book at the default level.
def getOrderBook(coinpair):
    global book
    book = public_client.get_product_order_book(coinpair)
    print 'order book for', coinpair
    for x in book:
        return x, ':', book[x]

# FUNCTION Displays balances, STILL NEEDS INTEGRATION TO GUI

def getBalances():
    list1 = auth_client.get_accounts()
    for row in list1:
        #print row['currency'], ':', row['balance']
        print row

#getBalances()

# FUNCTION helper function, takes a coins name and returns its ID ie 'ALGO' == 3724372`0
def getcurrencyId(coin):
    global coinId
    a = coin
    #print a
    curry = auth_client.get_accounts()
    for a in curry:
        if a['currency'] == coin:

            coinId = a['id']
            return coinId


#getcurrencyId("ALGO")
#print coinId

# FUNCTION Get a single balance by ID
def getAbalance(coinPair):
    currencyId = getcurrencyId(coinPair)
    global singlbal
    singlbal= auth_client.get_account(str(currencyId))
    return singlbal

#im here

def splitPairs(insi):
    global splits
    inputi = insi
    ssplit = inputi.replace('-', ' ')
    #ssplit = inputi.split('-')
    for word in ssplit:
        splits += word
    return splits

#splitPairs('ALGO-GBP')

def getPairBalances(coinpair):
    global balances

    c = []
    cat = splitPairs(coinpair)
    for word in cat.split():


        a = getcurrencyId(word)
        b = auth_client.get_account(str(a))
        #c.append(b["balance"])
        c.append(b)
        balances = c
    return balances

# getPairBalances("USDT-GBP")
# print balances

# FUNCTION Get a single currency history by ID
def viewHistory(coinPair):

    historyId = getcurrencyId(coinPair)

    fills_gen = auth_client.get_account_history(historyId)
    # Get all fills (will possibly make multiple HTTP requests)
    global x
    for x in fills_gen:
        x = list(fills_gen)
        return x

# FUNCTION generates a list of the coinbase ids for currencies available
def ids_list():
    ids = auth_client.get_accounts()
    for row in ids:
        print row['currency'], ':  ', row['id']


# FUNCTION get the price of a single coin/ currency pair
def getPrice(coinpair):
    dog = float(auth_client.get_product_ticker(product_id=coinpair)['price'])
    print coinpair, ': ', dog

#GUI#######################################

root = tk.Tk()
root.geometry("1400x600")
root.title('Bot Manager')
# place a label on the root windo
pageTitle = tk.Label(root, text="Bot Manager")
pageTitle.pack()



def loadData():
    global labelsarray

    singleStats = tk.Label(w, text=str(formatString(pair)))
    singleStats.pack(padx=5, pady=15, side=tk.LEFT)
    labelsarray.append(singleStats)

    twentyfourStats = tk.Label(x, text=str(formatString(day)))
    twentyfourStats.pack(padx=5, pady=15, side=tk.LEFT)
    labelsarray.append(twentyfourStats)

    getbook = tk.Label(y, text=str(formatString(book)))
    getbook.pack(padx=5, pady=15, side=tk.LEFT)
    labelsarray.append(getbook)

    getpairs = tk.Label(z, text=str(formatString(balances)))
    getpairs.pack(padx=5, pady=15, side=tk.LEFT)
    labelsarray.append(getpairs)

    # gethistory = tk.Label(z, text=str(formatString(x)))
    # gethistory.pack(padx=5, pady=15, side=tk.LEFT)
    # labelsarray.append(gethistory)
    #
    # getbalance = tk.Label(z, text=str(formatString(singlbal)))
    # getbalance.pack(padx=5, pady=15, side=tk.LEFT)
    # labelsarray.append(getbalance)




def submit():  # Callback function for SUBMIT Button
    global labelsarray
    global balances



    for i in labelsarray:
        i.destroy()


    global text
    text = textbox.get("1.0", 'end-1c')  # type: object # For line 1, col 0 to end.
    statsOnSingle(text)
    twentyFourStats(text)
    getOrderBook(text)
    getPairBalances(text)

    # viewHistory("USDC")
    # getAbalance("USDC") #will need its own button
    print balances
    loadData()
    # formatString(text)
    # splitPairs(text)

submitbutton = tk.Button(root, width=10, height=1, text='SUBMIT', command=submit)
submitbutton.pack()

textbox = tk.Text(root, width=30, height=2)
textbox.pack()

w = tk.Label(root, height=250, width=250,relief="raised", bg="grey")
w.pack(side=tk.LEFT)
x = tk.Frame(root, height=250, width=250,relief="raised", bg="grey")
x.pack(side=tk.LEFT)
y = tk.Frame(root, height=250, width=250,relief="raised", bg="grey")
y.pack(side=tk.LEFT)
z = tk.Frame(root, height=250, width=250,relief="raised", bg="grey")
z.pack(side=tk.LEFT)




# s = ttk.Style()
# s.configure('My.TFrame', background='red')






# quitbutton = tk.Button(root, width=10, height=1, text='QUIT', command=quit)
# quitbutton.pack()


root.mainloop()

# MyNaivebot ########################################## Needs its own class

# sell_price = 0.3300
# sell_amt = 38.0
#
# buy_price = 0.3000
# buy_amt = 38.0
#
# safety_price = (buy_price/3)*2
#
# print 'sell at:',sell_price, 'buy at:', buy_price, 'safety price:', safety_price
# while True:
#
#     price = float(auth_client.get_product_ticker(product_id='XLM-EUR')['price'])
#     print 'current price:', price
#     if price <= buy_price and price > safety_price:
#         print('buying XLM for')
#         auth_client.buy(size=buy_amt, order_type='market', product_id='XLM-EUR')
#     elif price >= sell_price:
#         auth_client.sell(size=sell_amt, order_type='market',product_id='XLM-EUR')
#         print('selling XLM')
#     else:
#         print('no orders placed')
#     time.sleep(180)


#####################################################################################################################