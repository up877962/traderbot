import cbpro
from Bot import Bot
import Tkinter as tk




# SORT OUT VARIABLE NAMES

data = open('keys.txt', 'r').read().splitlines()
public = data[0]
passphrase = data[1]
secret = data[2]
public_client = cbpro.PublicClient()
auth_client = cbpro.AuthenticatedClient(public, secret, passphrase)

# VARIABLES
new_input = ""
text = ""
newpair = {}
day = {}
book = {}
coinId = {}
singlbal = {}
x = []
labelsarray = []
splits = ""
balances = []
histories = []




# FUNCTION Enter a coin pairs such a algo gbp in the format 'ALGO-GBP'
def statsOnSingle(coinPair):
    global newpair
    pair = public_client.get_product_ticker(product_id=coinPair)  # type: dict
    newpair = pair

    #return newpair
    #return str(newpair)

def formatString(ins):
    new_input = str(ins)
    replaced = new_input.replace(',', '\n')
    return replaced


#####FUNCTION 24 Hour stats on a currency-coin pairing
def twentyFourStats(coinpair):
    global day
    day = public_client.get_product_24hr_stats(product_id=coinpair)
    a = day.keys()
    b = day.values()

    return a, b


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
    for order in book:
        return order


# FUNCTION Displays balances, STILL NEEDS INTEGRATION TO GUI
def getBalances():
    list1 = auth_client.get_accounts()
    for row in list1:
        print row


# FUNCTION helper function, takes a coins name and returns its ID ie 'ALGO' == 3724372`0
def getcurrencyId(coin):
    global coinId
    curry = auth_client.get_accounts()
    for a in curry:
        if a['currency'] == coin:
            coinId = a['id']
            return coinId


# FUNCTION Get a single balance by ID
def getAbalance(coinPair):
    currencyId = getcurrencyId(coinPair)
    global singlbal
    singlbal = auth_client.get_account(str(currencyId))
    return singlbal


def splitPairs(insi):
    global splits
    inputi = insi
    ssplit = inputi.replace('-', ' ')
    for word in ssplit:
        splits += word
    return splits


# FUNCTION Get a single currency history by ID
def viewHistory(coinPair):
    historyId = getcurrencyId(coinPair)
    fills_gen = auth_client.get_account_history(historyId)
    # Get all fills (will possibly make multiple HTTP requests)
    global x
    for x in fills_gen:
        x = list(fills_gen)
        return x


def getboth(coinpair):
    global histories
    a = splitPairs(coinpair)
    for i in a.split():
        b = viewHistory(i)
        histories.append(b)
    return histories


# FUNCTION generates a list of the coinbase ids for currencies available
def ids_list():
    ids = auth_client.get_accounts()
    for row in ids:
        print row['currency'], ':  ', row['id']


# FUNCTION get the price of a single coin/ currency pair
def getPrice(coinpair):
    dog = float(auth_client.get_product_ticker(product_id=coinpair)['price'])
    print coinpair, ': ', dog


def getPairBalances(coinpair):
    global balances
    c = []
    words = splitPairs(coinpair)
    for word in words.split():
        a = getcurrencyId(word)
        b = auth_client.get_account(str(a))
        c.append(b)
        balances = c
    return balances

# getPairBalances("USDT-GBP")


#a test of the bots function after being moved to its own class, parameters in order are, sell price,sell amnt, buy price
# , buy amnt, and trading pair -will change currency to first later
def botTest():
    bot = Bot(0.3300, 38.0, 0.3000, 38.0, 'XLM-EUR')
    bot.launcher()
#botTest


# GUI#######################################

root = tk.Tk()
# root.geometry("1400x700")
rootHeight = 600
rootWidth = 1400
root.title('Bot Manager')
# place a label on the root windo
# pageTitle = tk.Label(root, text="")
# pageTitle.pack()

leftframe = tk.LabelFrame(root,bg="grey",padx=5, pady=5,width=rootWidth/3, height= rootHeight-10)
leftframe.pack(padx=10,pady=10,side=tk.LEFT)
centreframe = tk.LabelFrame(root,bg="grey", padx=5, pady=5,width=rootWidth/3, height= rootHeight-10)
centreframe.pack(side=tk.TOP,padx=10, pady=10)
rightframe = tk.LabelFrame(root,bg="grey", padx=5, pady=5,width=rootWidth/3, height= rootHeight-10)
rightframe.pack(padx=10, pady=10,side=tk.LEFT)




centretitle = tk.Label(centreframe, text="Enter pair here in this format: algo-gbp, btc-eur to see stats in the left pane")
centretitle.pack()

righttitle = tk.Label(rightframe, text="Configure Bots in this panel, then launch when ready")
righttitle.pack()


sinstats = tk.Label(leftframe, text="Current stats")
sinstats.pack()
statssingleholder = tk.Text(leftframe, width=40, height=7,borderwidth=2, relief="groove", padx=5, pady=5)
statssingleholder.pack(pady= 10, padx= 10)
twenfrstats = tk.Label(leftframe, text="24 hour stats")
twenfrstats.pack()
statstwenfour = tk.Text(leftframe, width=40, height=6,borderwidth=2, relief="groove", padx=5, pady=5)
statstwenfour.pack(pady= 10, padx= 10)
orderlab = tk.Label(leftframe, text="Order book")
orderlab.pack()
orderbholder = tk.Text(leftframe, width=40, height=9,borderwidth=2, relief="groove", padx=5, pady=5)
orderbholder.pack(pady= 10, padx= 10)
pairslab = tk.Label(leftframe, text="balances")
pairslab.pack()
pairsholder = tk.Text(leftframe, width=40, height=10,borderwidth=2, relief="groove", padx=5, pady=5)
pairsholder.pack(pady= 10, padx= 10)

histoframe = tk.LabelFrame(root,bg="grey", padx=5, pady=5,width=rootWidth/3, height= rootHeight-10)
histoframe.pack(padx=10, pady=10,side=tk.LEFT)

# histlab = tk.Label(histoframe, text="History")
# histlab.pack()

histholder = tk.Text(histoframe, width=40, height=50,borderwidth=2, relief="groove")
histholder.pack(side=tk.LEFT)

scroll_bar = tk.Scrollbar(histoframe, orient="vertical",command=histholder.yview)
scroll_bar.pack(side=tk.RIGHT, expand=True, fill="y")
histholder.configure(yscrollcommand=scroll_bar.set)






# balholder = tk.Text(leftframe, width=40, height=5,borderwidth=2, relief="groove", padx=5, pady=5)
# balholder.pack(pady= 10, padx= 10)



#opens a new window containing the bots running data - not implemented yeet
def openNewWindow():
    newWindow = tk.Toplevel(root)
    newWindow.title("new window")
    newWindow.geometry("200x200")
    tk.Label(newWindow,
          text="").pack()


def loadData():
    global labelsarray
    global balances
    global histories

    statssingleholder.insert('1.0', formatString(newpair))
    statstwenfour.insert('1.0', formatString(day))
    orderbholder.insert('1.0', formatString(book))
    pairsholder.insert('1.0', formatString(balances))
    histholder.insert('1.0', formatString(histories))
    #balholder.insert('1.0', singlbal)


def submit():  # Callback function for SUBMIT Button
    global text
    global labelsarray
    for i in labelsarray:
        i.destroy()

    text = textbox.get("1.0", 'end-1c').upper()

    getPairBalances(text)
    statsOnSingle(text)
    twentyFourStats(text)
    getOrderBook(text)
    getboth(text)
    # getAbalance("USDC") #will need its own button

    loadData()




selectorframe = tk.LabelFrame(rightframe,bg="grey", padx=5, pady=5)
selectorframe.pack(padx=10, pady=10,side=tk.LEFT)

botselecttext = tk.Label(selectorframe, text="choose the type of bot to deploy")
botselecttext.pack()

naivebot = tk.Label(selectorframe, text="Naive bot")
naivebot.pack()
xradio = tk.Radiobutton(selectorframe, width=15, height=1)
xradio.pack()
nextbot = tk.Label(selectorframe, text="Not yet bot")
nextbot.pack()
yradio = tk.Radiobutton(selectorframe, width=15, height=1)
yradio.pack()
nextbota = tk.Label(selectorframe, text="Nope bot")
nextbota.pack()
zradio = tk.Radiobutton(selectorframe, width=15, height=1)
zradio.pack()
nextbotb = tk.Label(selectorframe, text="you wish bot")
nextbotb.pack()
qradio = tk.Radiobutton(selectorframe, width=15, height=1)
qradio.pack()



buttonsframe = tk.LabelFrame(rightframe,bg="grey", padx=5, pady=5)
buttonsframe.pack(padx=10, pady=10,side=tk.LEFT)






sellp = tk.Label(buttonsframe, text="enter the sell price")
sellp.pack()
sellpricebox = tk.Text(buttonsframe, width=5, height=1)
sellpricebox.pack()


sellam = tk.Label(buttonsframe, text="enter the sell amount")
sellam.pack()
sellamntbox = tk.Text(buttonsframe, width=5, height=1)
sellamntbox.pack()

buyp = tk.Label(buttonsframe, text="enter the buy price")
buyp.pack()
buypricebox = tk.Text(buttonsframe, width=5, height=1)
buypricebox.pack()

buyam = tk.Label(buttonsframe, text="enter the buy amount")
buyam.pack()
buyamntbox = tk.Text(buttonsframe, width=5, height=1)
buyamntbox.pack()


currancylab = tk.Label(buttonsframe, text="enter the currency pair")
currancylab.pack()
currencybox = tk.Text(buttonsframe, width=15, height=1)
currencybox.pack()

textdesc = tk.Text(rightframe, width=40, height=10,borderwidth=2, relief="groove", padx=5, pady=5)
textdesc.pack(pady= 10, padx= 10)

textbox = tk.Text(centreframe, width=30, height=2)
textbox.pack()


submitbutton = tk.Button(centreframe, width=10, height=1, text='SUBMIT', command=submit)
submitbutton.pack()

btn = tk.Button(rightframe,text="Submit\n(A new window will open showing data from it)",command = openNewWindow)
btn.pack(pady= 10, padx= 100, side=tk.BOTTOM)




# quitbutton = tk.Button(root, width=10, height=1, text='QUIT', command=quit)
# quitbutton.pack()


root.mainloop()

