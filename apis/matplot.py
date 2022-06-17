import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
import pandas as pd

def plot_candle(df,stock_code):
    # df = df.sort_index()
    # df.index = pd.to_datetime(df['trade_date'])
    df['_date'] = df.apply(lambda x: x['trade_date'][-6:] ,axis=1)

    fig, ax = plt.subplots(2,1)
    ax[0].plot(df['_date'], df['hlc3'],label='hlc3')
    ax[0].plot(df['_date'], df['ema_upper'],label='boollinger_upper')
    ax[0].plot(df['_date'], df['ema_lower'],label='boollinger_lower')
    ax[0].plot(df['_date'], df['ema'],label='boollinger_middle')
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Price')
    ax[0].set_title(stock_code)
    ax[0].invert_xaxis()
    ax[0].legend()

    ax[1].set_title(stock_code)
    ax[1].plot(df['_date'], df['bandwidth'],label='bandwidth')
    plt.savefig('img/'+stock_code+'.png')
    plt.show()

def plot_scatter(df,xkey,ykey,title):
    fig, ax = plt.subplots()
    ax.scatter(df[xkey],df[ykey],vmin=0, vmax=100)
    ax.set_xlabel(xkey)
    ax.set_ylabel(ykey)
    ax.set_title(title)
    plt.show()

def plot_boolinger(df,stock_code):
    df['_date'] = df.apply(lambda x: x['trade_date'][-6:] ,axis=1)
    fig, ax = plt.subplots()
    ax.plot(df['_date'], df['hlc3'],label='hlc3')
    ax.plot(df['_date'], df['ema_upper'],label='boollinger_upper')
    ax.plot(df['_date'], df['ema_lower'],label='boollinger_lower')
    ax.plot(df['_date'], df['ema'],label='boollinger_middle')
    ax.set_xlabel('Date')
    ax.set_ylabel('Price')
    ax.set_title(stock_code)
    ax.invert_xaxis()
    ax.legend()
    # plt.savefig('img/'+stock_code+'.png')
    plt.show()

# plot_candle(pd.read_csv('stock/testing.csv', index_col=0), '000960.SZ')