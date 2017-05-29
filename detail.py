# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from urllib.request import urlopen
from pytz import timezone
from datetime import datetime
from graph import graph_data
import pyimgur


# def get_data(stock_name):
#     link_daily_quote = 'http://marketdata.set.or.th/mkt/stockquotation.do?symbol=' + stock_name + '&ssoPageId=1&language=en&country=US'
#     link_historical_trading = 'http://www.set.or.th/set/historicaltrading.do?symbol=' + stock_name + '&ssoPageId=2&language=en&country=US'
#     link_profile = 'http://www.set.or.th/set/companyprofile.do?symbol=' + stock_name + '&ssoPageId=4&language=en&country=US'
#     link_highlights = 'http://www.set.or.th/set/companyhighlight.do?symbol=' + stock_name + '&ssoPageId=5&language=en&country=US'
#     link_holder = 'http://www.set.or.th/set/companyholder.do?symbol=' + stock_name + '&ssoPageId=6&language=en&country=US'
#     link_rights = 'http://www.set.or.th/set/companyrights.do?symbol=' + stock_name + '&ssoPageId=7&language=en&country=US'
#     link_news = 'http://www.set.or.th/set/companynews.do?symbol=' + stock_name + '&ssoPageId=8&language=en&country=US'
#
#     r_daily_quote = urlopen(link_daily_quote).read()
#     r_historical_trading = urlopen(link_historical_trading).read()
#     r_profile = urlopen(link_profile).read()
#     r_highlights = urlopen(link_highlights).read()
#     r_holder = urlopen(link_holder).read()
#     r_rights = urlopen(link_rights).read()
#     r_news = urlopen(link_news).read()
#
#     soup_daily_quote = BeautifulSoup(r_daily_quote)
#     soup_historical_trading = BeautifulSoup(r_historical_trading)
#     soup_profile = BeautifulSoup(r_profile)
#     soup_highlights = BeautifulSoup(r_highlights)
#     soup_holder = BeautifulSoup(r_holder)
#     soup_rights = BeautifulSoup(r_rights)
#     soup_news = BeautifulSoup(r_news)
#
#     ret_dict = {}
#     ret_dict['daily_quote'] = soup_daily_quote
#     ret_dict['historical_trading'] = soup_historical_trading
#     ret_dict['profile'] = soup_profile
#     ret_dict['highlights'] = soup_highlights
#     ret_dict['holder'] = soup_holder
#     ret_dict['rights'] = soup_rights
#     ret_dict['news'] = soup_news
#     return ret_dict

def remove_unness(col):
    col = [str(s).replace("<td>", "") for s in col]
    col = [str(s).replace("</td>", "") for s in col]
    col = [str(s).replace('<td class="loser">', "") for s in col]
    col = [str(s).replace('<td class="gainer">', "") for s in col]
    col = [str(s).replace('<td class="nochange">', "") for s in col]
    col = [str(s).replace('<td style="text-align: left;">', "") for s in col]
    col = [str(s).replace('<td style="text-align: center;">', "") for s in col]
    col = [str(s).replace('</a>', "") for s in col]
    col = [str(s).replace('<font>', "") for s in col]
    col = [str(s).replace('</font>', "") for s in col]
    col = [str(s).split('>', 1)[-1] for s in col]
    col = [s.strip(' \t\n\r') for s in col]
    col = [s.replace(' ', '') for s in col]
    return col


def daily_quote(stock_name):
    link_daily_quote = 'http://marketdata.set.or.th/mkt/stockquotation.do?symbol=' + stock_name + '&ssoPageId=1&language=en&country=US'
    r_daily_quote = urlopen(link_daily_quote).read()
    soup_daily_quote = BeautifulSoup(r_daily_quote)
    table_body = soup_daily_quote.find('tbody')
    rows = table_body.find_all('tr')
    ret_dict = {}
    for row in rows:
        cols = row.find_all('td')
        for i, td in enumerate(cols):
            text = cols[i].renderContents().strip()
            if str(text) == "b'Last'":
                last = cols[i + 1].renderContents().strip()
                last = str(last).split('>', 1)[-1]
                last = str(last).split('>', 1)[-1]
                last = str(last).replace("b'", "")
                last = last[:-1]
                ret_dict['last'] = last
            elif str(text) == "b'Open'":
                open = cols[i + 1].renderContents().strip()
                open = str(open)[2:-2]
                ret_dict['open'] = open
            elif str(text) == "b'High'":
                high = cols[i + 1].renderContents().strip()
                high = str(high)[2:-2]
                ret_dict['high'] = high
            elif str(text) == "b'Low'":
                low = cols[i + 1].renderContents().strip()
                low = str(low)[2:-2]
                ret_dict['low'] = low
            elif str(text)[:8] == "b'Volume":
                volume = cols[i + 1].renderContents().strip()
                volume = str(volume)[2:-1]
                ret_dict['volume'] = volume
            elif str(text)[:7] == 'b"Value':
                value = cols[i + 1].renderContents().strip()
                value = str(value)[2:-1]
                ret_dict['value'] = value
    return ret_dict


def profile(stock_name):
    link_profile = 'http://www.set.or.th/set/companyprofile.do?symbol=' + stock_name + '&ssoPageId=4&language=en&country=US'
    r_profile = urlopen(link_profile).read()
    soup_profile = BeautifulSoup(r_profile)
    table_body = soup_profile.find('table')
    ret_dict = {}
    rows = table_body.find_all('div')
    for i, content in enumerate(rows):
        text = content.renderContents().strip()
        # print(text)
        if str(text)[2:5] == "P/E":
            pe = rows[i + 1].renderContents().strip()
            pe = str(pe)[2:-1]
            ret_dict['P/E'] = pe
        elif str(text)[2:6] == "P/BV":
            pbv = rows[i + 1].renderContents().strip()
            pbv = str(pbv)[2:-1]
            ret_dict['P/BV'] = pbv
        elif str(text)[2:5] == "Dvd":
            dvd = rows[i + 1].renderContents().strip()
            dvd = str(dvd)[2:-1]
            ret_dict['Dividend Yield(%)'] = dvd
        elif str(text) == "b'<strong>Market</strong>'":
            market = rows[i + 1].renderContents().strip()
            market = str(market)[2:-1]
            ret_dict['Market'] = market
        elif str(text) == "b'<strong>Industry</strong>'":
            industry = rows[i + 1].renderContents().strip()
            industry = str(industry)[2:-1]
            ret_dict['Industry'] = industry
        elif str(text) == "b'<strong>Sector</strong>'":
            sector = rows[i + 1].renderContents().strip()
            sector = str(sector)[2:-1]
            sector = str(sector).replace("amp;", "")
            ret_dict['Sector'] = sector
    return ret_dict


def get_stock_data(stock_name):
    try:
        dq = daily_quote(stock_name)
        pf = profile(stock_name)
        graph_data(stock_name)
        CLIENT_ID = "3c233163a097e9e"
        PATH = "temp.png"

        im = pyimgur.Imgur(CLIENT_ID)
        uploaded_image = im.upload_image(PATH, title="Chart with PyImgur")
        print(uploaded_image.link)
        message = {
            "messages": [
                {"text": u" --- Stock Information --- "
                         + u"\nMarket: " + pf['Market']
                         + u"\nIndustry: " + pf['Industry']
                         + u"\nSector: " + pf['Sector']
                         + u"\nDividend Yield(%): " + pf['Dividend Yield(%)']
                         + u"\nP/E: " + pf['P/E'] + u"\nP/BV: " + pf['P/BV']
                 },
                {"text": u" --- Last Quote --- "
                         + u"\nlast: " + dq['last']
                         + u"\nopen: " + dq['open']
                         + u"\nhigh: " + dq['high']
                         + u"\nlow: " + dq['low']
                         + u"\nvolume: " + dq['volume']
                         + u"\nvalue: " + dq['value']
                 },
                {"attachment":
                    {
                        "type": "image",
                        "payload": {"url": uploaded_image.link}
                    }
                }
            ]
        }
    except Exception as e:
        message = {
            "messages": [
                {"text": u" I think you enter incorrect stock name  !! "}
            ]
        }
    return message


def trading_summary():
    link_profile = 'http://marketdata.set.or.th/mkt/investortype.do?language=en&country=US'
    r_profile = urlopen(link_profile).read()
    soup_profile = BeautifulSoup(r_profile)
    table_body = soup_profile.find('table')
    rows = table_body.find_all('tbody')
    rows = rows[0].find_all('tr')
    message = {}
    buy = []
    sell = []
    summ = []
    for i, content in enumerate(rows):
        col = content.find_all('td')
        col = [str(s).replace("<td>", "") for s in col]
        col = [str(s).replace("</td>", "") for s in col]
        col = [str(s).replace('<td class="loser">', "") for s in col]
        col = [str(s).replace('<td class="gainer">', "") for s in col]
        col = [s.strip('\r') for s in col]
        col = [s.strip('\n') for s in col]
        # print(col[1], col[3], "".join(col[5].split()))
        buy.append("".join(col[1].split()))
        sell.append("".join(col[3].split()))
        summ.append("".join(col[5].split()))
    # print(buy[0], sell[0], summ[0])
    # print(buy[1], sell[1], summ[1])
    # print(buy[2], sell[2], summ[2])
    # print(buy[3], sell[3], summ[3])
    message['messages'] = [
        {
            "text": u"Trading Summary" +
                    u"\nInsti..\t\t" + summ[0] +
                    u"\nProp...\t\t" + summ[1] +
                    u"\nForeign\t\t" + summ[2] +
                    u"\nIndividual\t\t" + summ[3]
            # + u"\n**หน่วย:ล้านบาท\nข้อมูล ณ วันที่" + str(datetime.now(timezone('Asia/Bangkok')))
        }
    ]
    return message


def tfex_summary():
    link_profile = 'http://marketdata.set.or.th/tfx/tfexintradayreport.do?locale=th_TH'
    r_profile = urlopen(link_profile).read()
    soup_profile = BeautifulSoup(r_profile)
    table_body = soup_profile.find('table')
    rows = table_body.find_all('tbody')
    rows = rows[0].find_all('tr')
    message = {}
    name = []
    date = []
    opn = []
    high = []
    low = []
    bid = []
    off = []
    last = []
    percent = []
    for i, content in enumerate(rows):
        col = content.find_all('td')
        try:
            col = [str(s).replace("<td>", "") for s in col]
            col = [str(s).replace("</td>", "") for s in col]
            col = [str(s).replace('<td class="loser">', "") for s in col]
            col = [str(s).replace('<td class="gainer">', "") for s in col]
            col = [str(s).replace('<td class="nochange">', "") for s in col]
            col = [str(s).replace('<td style="text-align: left;">', "") for s in col]
            col = [str(s).replace('<td style="text-align: center;">', "") for s in col]
            col = [s.strip(' \t\n\r') for s in col]
            col = [s.replace(' ', '') for s in col]
            # print(col[0],col[1],col[2],col[3],col[4],col[5],col[6],col[7],col[8])
            name.append(col[0])
            date.append(col[1])
            opn.append(col[2])
            high.append(col[3])
            low.append(col[4])
            bid.append(col[5])
            off.append(col[6])
            last.append(col[7])
            percent.append(col[8])
        except:
            pass
    message['messages'] = [
        {"text": u"Symbol: " + name[2] + u"\nContract Month: " + date[
            1] + u"\n\nopen: " + opn[1] + u"\nhigh: " + high[1] + u"\nlow: " + low[
                     1] + u"\n\nlast: " + last[1] + u"\nBID: " + bid[1] + u"\nOFFER: " + off[
                     1] + u"\nchange: " + percent[1]},
        {"text": u"Symbol: " + name[3] + u"\nContract Month: " + date[
            2] + u"\n\nopen: " + opn[2] + u"\nhigh: " + high[2] + u"\nlow: " + low[
                     2] + u"\n\nlast: " + last[2] + u"\nBID: " + bid[2] + u"\nOFFER: " + off[
                     2] + u"\nchange: " + percent[2]},
        {"text": u"Symbol: " + name[4] + u"\nContract Month: " + date[
            3] + u"\n\nopen: " + opn[3] + u"\nhigh: " + high[3] + u"\nlow: " + low[
                     3] + u"\n\nlast: " + last[3] + u"\nBID: " + bid[3] + u"\nOFFER: " + off[
                     3] + u"\nchange: " + percent[3]},
        {"text": u"Symbol: " + name[5] + u"\nContract Month: " + date[
            4] + u"\n\nopen: " + opn[4] + u"\nhigh: " + high[4] + u"\nlow: " + low[
                     4] + u"\n\nlast: " + last[4] + u"\nBID: " + bid[4] + u"\nOFFER: " + off[
                     4] + u"\nchange: " + percent[4]},
        {"text": u"Symbol: " + name[6] + u"\nContract Month: " + date[
            5] + u"\n\nopen: " + opn[5] + u"\nhigh: " + high[5] + u"\nlow: " + low[
                     5] + u"\n\nlast: " + last[5] + u"\nBID: " + bid[5] + u"\nOFFER: " + off[
                     5] + u"\nchange: " + percent[5]}

    ]
    return message


def set_realtime_summary():
    link_profile = 'http://marketdata.set.or.th/mkt/marketsummary.do?language=th&country=TH'
    r_profile = urlopen(link_profile).read()
    soup_profile = BeautifulSoup(r_profile)
    table_body = soup_profile.find('table')
    rows = table_body.find_all('tbody')
    rows = rows[0].find_all('tr')
    message = {}
    name = []
    last = []
    chg = []
    percent = []
    high = []
    low = []
    for i, content in enumerate(rows):
        col = content.find_all('td')
        try:
            col = remove_unness(col)
            # print(col[0], col[1], col[2], col[3], col[4], col[5])
            name.append(col[0])
            last.append(col[1])
            chg.append(col[2])
            percent.append(col[3])
            high.append(col[4])
            low.append(col[5])
        except:
            pass
    message['messages'] = [
        {"text": u"index: " + name[5] + u"\nlast: " + last[5] + u"\n\nchange: " + chg[5] + u"(" + percent[
            5] + u"%)" + u"\nhigh: " + high[5] + u"\nlow: " + low[5]},
        {"text": u"index: " + name[4] + u"\nlast: " + last[4] + u"\n\nchange: " + chg[4] + u"(" + percent[
            4] + u"%)" + u"\nhigh: " + high[4] + u"\nlow: " + low[4]},
        {"text": u"index: " + name[3] + u"\nlast: " + last[3] + u"\n\nchange: " + chg[3] + u"(" + percent[
            3] + u"%)" + u"\nhigh: " + high[3] + u"\nlow: " + low[3]},
        {"text": u"index: " + name[2] + u"\nlast: " + last[2] + u"\n\nchange: " + chg[2] + u"(" + percent[
            2] + u"%)" + u"\nhigh: " + high[2] + u"\nlow: " + low[2]},
        {"text": u"index: " + name[1] + u"\nlast: " + last[1] + u"\n\nchange: " + chg[1] + u"(" + percent[
            1] + u"%)" + u"\nhigh: " + high[1] + u"\nlow: " + low[1]},
        {"text": u"index: " + name[0] + u"\nlast: " + last[0] + u"\n\nchange: " + chg[0] + u"(" + percent[
            0] + u"%)" + u"\nhigh: " + high[0] + u"\nlow: " + low[0]}
    ]
    return message
