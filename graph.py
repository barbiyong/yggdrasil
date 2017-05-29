import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.finance import candlestick_ohlc
import pandas as pd
import numpy as np
import datetime


def get_stock_data(stock_name, time_frame):
    tmp_list = {}
    data_list = dict()
    candle_length = 200
    url_d = 'http://devapi.marketanyware.com/Test/OHLC.aspx?DL=1&Stock=' + stock_name + '&period=day'
    url_w = 'http://devapi.marketanyware.com/Test/OHLC.aspx?DL=1&Stock=' + stock_name + '&period=week'
    url_m = 'http://devapi.marketanyware.com/Test/OHLC.aspx?DL=1&Stock=' + stock_name + '&period=month'
    url_1h = 'http://devapi.marketanyware.com/Test/OHLC.aspx?DL=1&Stock=' + stock_name + '&period=Hour'
    url_2h = 'http://devapi.marketanyware.com/Test/OHLC.aspx?DL=1&Stock=' + stock_name + '&period=2Hour'

    if time_frame is 'day':
        url = url_d
    elif time_frame is 'week':
        url = url_w
    elif time_frame is 'month':
        url = url_m
    elif time_frame is 'hour':
        url = url_1h
    elif time_frame is '2Hour':
        url = url_2h

    try:
        stock_data_input = pd.io.parsers.read_csv(url, sep=',')
    except pd.io.common.CParserError:
        return None

    tmp_list['date'] = np.array(stock_data_input['Date'])

    if len(tmp_list['date']) < candle_length:
        candle_length = len(tmp_list['date'])

    # get data from web
    data_list['date'] = np.array(stock_data_input['Date'])
    data_list['open'] = np.array(stock_data_input['Op'])
    data_list['high'] = np.array(stock_data_input['High'])
    data_list['low'] = np.array(stock_data_input['Low'])
    data_list['close'] = np.array(stock_data_input['Close'])
    data_list['volume'] = np.array(stock_data_input['Volume'])

    data_length = len(data_list['date'])


    ret_list = []
    for i,date in enumerate(data_list['date']):
        dateymd = datetime.datetime.strptime(data_list['date'][i], '%m/%d/%Y').strftime('%Y%m%d')
        ret_list.append(
            str(dateymd)+str(',')+str(data_list['close'][i])+str(',')+str(data_list['high'][i])+str(',')+str(data_list['low'][i])+str(',')+str(data_list['open'][i])+str(',')+str(data_list['volume'][i])
        )
    return ret_list[-50:]


def bytespdate2num(fmt, encoding='utf-8'):
    strconverter = mdates.strpdate2num(fmt)

    def bytesconverter(b):
        s = b.decode(encoding)
        return strconverter(s)

    return bytesconverter


def graph_data(stock):
    fig = plt.figure()
    ax1 = plt.subplot2grid((1, 1), (0, 0))

    stock_data = get_stock_data(stock, 'day')
    print(stock_data)
    date, closep, highp, lowp, openp, volume = np.loadtxt(stock_data,
                                                          delimiter=',',
                                                          unpack=True,
                                                          converters={0: bytespdate2num('%Y%m%d')})

    x = 0
    y = len(date)
    ohlc = []

    while x < y:
        append_me = date[x], openp[x], highp[x], lowp[x], closep[x], volume[x]
        ohlc.append(append_me)
        x += 1

    candlestick_ohlc(ax1, ohlc, width=0.7, colorup='#77d879', colordown='#db3f3f')

    for label in ax1.xaxis.get_ticklabels():
        label.set_rotation(75)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    ax1.xaxis.set_major_locator(mticker.MaxNLocator(10))
    ax1.grid(True)

    plt.xlabel('Date')
    plt.ylabel('Price')
    plt.title(stock)
    plt.legend()
    plt.subplots_adjust(left=0.09, bottom=0.20, right=0.94, top=0.90, wspace=0.2, hspace=0)
    # plt.show()
    fig.savefig('temp.png', bbox_inches='tight')

# graph_data('TMI')