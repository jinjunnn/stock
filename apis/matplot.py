import matplotlib.pyplot as plt
import matplotlib.cbook as cbook
from matplotlib.pyplot import MultipleLocator
import pandas as pd

def plot_candle(df,stock_code):
    # df['_date'] = df.apply(lambda x: x['trade_date'][-6:] ,axis=1)

    fig, ax = plt.subplots(2,1)
    ax[0].plot(df['trade_date'], df['hlc3'],label='hlc3')
    ax[0].plot(df['trade_date'], df['ema_upper'],label='boollinger_upper')
    ax[0].plot(df['trade_date'], df['ema_lower'],label='boollinger_lower')
    ax[0].plot(df['trade_date'], df['ema'],label='boollinger_middle')
    ax[0].set_xlabel('Date')
    ax[0].set_ylabel('Price')
    ax[0].set_title(stock_code)
    ax[0].legend()# 添加图标说明
    ax[0].xaxis.set_major_locator(MultipleLocator(10))# 添加刻度
    # ax[0].invert_xaxis()# 旋转X轴方向

    ax[1].set_title(stock_code)
    
    ax[1].plot(df['trade_date'], df['bandwidth'],label='bandwidth')
    ax[1].xaxis.set_major_locator(MultipleLocator(10))
    # ax[1].invert_xaxis()
    # plt.savefig('img/'+stock_code+'.png')
    plt.show()

def plot_scatter(df,xkey,ykey,title):
    fig, ax = plt.subplots()
    ax.scatter(df[xkey],df[ykey],vmin=0, vmax=100)
    ax.set_xlabel(xkey)
    ax.set_ylabel(ykey)
    ax.set_title(title)
    axs.xaxis.set_major_locator(MultipleLocator(40))
    plt.show()

def plot_alligator(df,stock_code):
    fig, axs = plt.subplots(2, 1)
    axs[0].plot(df['trade_date'], df['close'],label='close')
    axs[0].plot(df['trade_date'], df['jaw'],label='jaw')
    axs[0].plot(df['trade_date'], df['teeth'],label='teeth')
    axs[0].plot(df['trade_date'], df['lips'],label='lips')
    axs[0].plot(df['trade_date'], df['ema144'],label='ema144')
    axs[0].plot(df['trade_date'], df['ema169'],label='ema169')
    axs[0].set_ylabel('Price')
    axs[0].set_title(stock_code)
    axs[0].xaxis.set_major_locator(MultipleLocator(40))    #设置时间刻度
    # ax.invert_xaxis() // 切换X轴方向
    axs[0].legend()

    axs[1].set_title('volume')
    axs[1].bar(df['trade_date'], df['vol'],label='vol')
    #设置时间刻度
    axs[1].xaxis.set_major_locator(MultipleLocator(40))
    plt.show()



def plot_boolinger(df,stock_code):
    fig, axs = plt.subplots(4, 1)
    axs[0].plot(df['time_key'], df['hlc3'],label='hlc3')
    axs[0].plot(df['time_key'], df['ema_upper'],label='boollinger_upper')
    axs[0].plot(df['time_key'], df['ema_lower'],label='boollinger_lower')
    axs[0].plot(df['time_key'], df['ema'],label='boollinger_middle')
    axs[0].set_ylabel('Price')
    axs[0].set_title(stock_code)
    #设置时间刻度
    axs[0].xaxis.set_major_locator(MultipleLocator(40))
    # ax.invert_xaxis() // 切换X轴方向
    axs[0].legend()

    axs[1].set_title('volume')
    axs[1].bar(df['time_key'], df['volume'],label='volume')
    #设置时间刻度
    axs[1].xaxis.set_major_locator(MultipleLocator(40))

    axs[2].set_title('volatility oscillator')
    axs[2].plot(df['time_key'], df['spike'],label='spike')
    axs[2].plot(df['time_key'], df['spike_upper'],label='spike_upper')
    axs[2].plot(df['time_key'], df['spike_lower'],label='spike_lower')
    axs[2].legend()
    #设置时间刻度
    axs[2].xaxis.set_major_locator(MultipleLocator(40))


    axs[3].set_title('macd')
    axs[3].plot(df['time_key'], df['macd'],label='macd')
    axs[3].plot(df['time_key'], df['signal'],label='signal')
    axs[3].bar(df['time_key'], df['histogram'],label='histogram')
    axs[3].legend()
    axs[3].xaxis.set_major_locator(MultipleLocator(40))
    # plt.savefig('img/'+stock_code+'.png')
    plt.show()

# plot_candle(pd.read_csv('stock/testing.csv', index_col=0), '000960.SZ')