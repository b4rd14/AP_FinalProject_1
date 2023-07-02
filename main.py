import  pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
from StockDB import get_user, update_user_balance

data = pd.read_csv('StockMarket/stock_market_data.csv')

# set log for user with all the transactions


def increaseBalance(user, amount):
    if user == None:
        print("User not found")
        return False
    user.balance += amount
    update_user_balance(user)
    return True

def set_log(user, date, volume, company_name, transaction_type):
    if user == None:
        print("User not found")
        return False
    user.history.append([date, volume, company_name, transaction_type])
    return True

def set_stock(user,company_name,volume,transaction_type):
    if user == None:
        print("User not found")
        return False
    else:
        if transaction_type == "buy":
            user.stocks[company_name] += volume
        else:
            user.stocks[company_name] -= volume
        return True



def buy_stock(user,date,volume,company_name):
    # Check if user has enough balance
    if user == None:
        print("User not found")
        return False
    if user.balance < data[data['Symbol'] == company_name]['Open'].iloc[-1] * volume:
        print("Not enough balance")
        return False
    # Check if stock is available
    if volume > data[data['Symbol'] == company_name]['Volume'].iloc[-1]:
        print("Not enough stock")
        return False
    # Update user balance 
    set_log(user, date, volume, company_name, "buy")
    set_stock(user,company_name,volume,"buy")
    user.balance -= data[data['Symbol'] == company_name]['Open'].iloc[-1] * volume
    update_user_balance(user)
    # Update stock volume
    data.loc[(data['Symbol'] == company_name) & (data['Date'] == date), 'Volume'] -= volume
    return True



def sell_stock(user,date,volume,company_name):
    # Check if user has enough stock
    if user == None:
        print("User not found")
        return False
    if volume > data[data['Symbol'] == company_name]['Volume'].iloc[-1]:
        print("Not enough stock")
        return False
    # Update user balance
    set_log(user, date, volume, company_name, "sell")
    set_stock(user,company_name,volume,"sell")
    user.balance += data[data['Symbol'] == company_name]['Open'].iloc[-1] * volume
    update_user_balance(user)
    # Update stock volume
    data.loc[(data['Symbol'] == company_name) & (data['Date'] == date), 'Volume'] += volume
    return True


buy_stock(get_user(1),"2019-01-02",10,"AAPL")
sell_stock(get_user(1),"2019-01-02",10,"AAPL")
buy_stock(get_user(1),"2019-01-02",5,"AAPL") 
buy_stock(get_user(1),"2019-01-02",5,"AAPL") 
buy_stock(get_user(1),"2010-08-24",5,"AMZN")


# Show the list of available stocks for each company
def showAvailableStocks():
    df_list=[]
    for company in data['Symbol'].unique():
        df = data[data['Symbol'] == company]
        df = df[['Date', 'Open', 'Volume']]
        df = df[df['Volume'] != 0]
        changes =[]
        for i in range(len(df['Open']) - 1):
            dict={"Date":df['Date'].iloc[i+1],"Yesterday": df['Date'].iloc[i] ,"Change":(df['Open'].iloc[i+1] - df['Open'].iloc[i]) / df['Open'].iloc[i] * 100}
            changes.append(dict)
        df = pd.DataFrame(changes)
        df['Date'] = pd.to_datetime(df['Date'])
        df = df.set_index('Date')
        df_list.append(df)
    
    fig, axes = plt.subplots(nrows=5, ncols=1, figsize=(16, 10) , sharey=True, sharex=True, constrained_layout=True)
    for i in range(len(df_list)):
        df_list[i].plot(ax=axes[i], title=data['Symbol'].unique()[i])
    plt.show()

    total_list = [] 
    for df in df_list:
        df = pd.DataFrame(df, columns=['Yesterday', 'Change'])
        df  = df.sort_values(by=['Change'] , ascending=False)
        total_list.append(df)

    return total_list

a = showAvailableStocks()

print(a[0])



# show the list of available stocks 
def overAllValue(user):
    value = 0
    for stock in user.history:
        if stock[3] == "buy":
            value += stock[1] * data[data['Symbol'] == stock[2]]['Open'].iloc[-1]
        else:
            value -= stock[1] * data[data['Symbol'] == stock[2]]['Open'].iloc[-1]
    
    plt.pie(user.stocks.values(), labels=user.stocks.keys(), autopct='%1.1f%%')
    plt.show()

    return value

overAllValue(get_user(1))

def showCompanyChanges(company_name):
    df = data[data['Symbol'] == company_name]
    df = df[['Date', 'Open']]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    df.plot(figsize=(16, 10), title=company_name)
    plt.show()

showCompanyChanges("GOOGL")


def showGeneralChanges():
    df = data[['Date', 'Open']]
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.set_index('Date')
    sns.regplot(x=mdates.date2num(df.index.values), y=df['Open'], color="green" , marker="+", scatter_kws={'s': 10})
    plt.show()

showGeneralChanges()