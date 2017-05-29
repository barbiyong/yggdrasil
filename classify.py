from decimal import Decimal
import get_template_result as gtr
import indicators as indi
import pandas as pd
import numpy as np

from sklearn.metrics import accuracy_score

from models import *

import warnings
warnings.filterwarnings("ignore")


def feature_result(data):
    # print(data)
    ohlc = [np.array(i, dtype=float) for i in data[:-1]]
    ohlc = np.vstack(ohlc).T
    ohlc = pd.DataFrame(data=ohlc, columns=['Open', 'Close', 'High', 'Low'])
    ohlc = indi.MACD(df=ohlc, n_fast=12, n_slow=26)
    ohlc = indi.RSI(df=ohlc, n=14)
    macd_diff = ohlc[-1:]['MACDdiff_12_26'].values.T.tolist()
    macd_diff = (1 if macd_diff[0] >= 0 else 0)
    last_rsi = round(ohlc[-1:]['RSI_14'].values.T.tolist()[0] * 100, 2)
    # print(macd_diff, last_rsi)
    return macd_diff, last_rsi


def pepare_data(data):
    x_a = []
    x_b = []
    y = []
    for i, name in enumerate(data['stock_name']):
        ismacdup, get_rsi_14 = feature_result(data['data'][i])
        x_a.append(ismacdup)
        x_b.append(get_rsi_14)
        y.append(data['retval'][i])

    x_a = np.array(x_a)
    x_b = np.array(x_b)
    y = np.array(y)

    features = np.vstack([x_a, x_b]).T
    output = np.hstack([y]).T

    return features, output


def get_test_data(data):
    x_a = []
    x_b = []
    for i, name in enumerate(data['stock_name']):
        ismacdup, get_rsi_14 = feature_result(data['data'][i])
        x_a.append(ismacdup)
        x_b.append(get_rsi_14)

    x_a = np.array(x_a)
    x_b = np.array(x_b)

    features = np.vstack([x_a, x_b]).T

    return features


def classify(stock_type, growth, lose, periods):
    # print(stock_type)
    ret_json = []
    result = gtr.get_growth_stock(stock_type, growth, lose, periods)
    # print(result)
    print('scanner get', result['stock_name'])
    print('PREPARE DATA ...')
    # print(result['Close'])
    X, Y = pepare_data(result)
    test_data = gtr.get_feature(stock_type, periods)
    X_test = get_test_data(test_data)
    y_train, y_test = fit_predict_RandomForestClassifier(X, Y, X_test)
    # print(y_train)
    # print(y_test)
    print('RandomForestClassifier\n', y_train, 'Train Accuracy:', accuracy_score(Y, y_train), '\n', y_test)
    for i, r in enumerate(y_test[:20]):
        if r == 1:
            ret_json.append(test_data['stock_name'][i])
    message = dict()
    msg = str(ret_json)[1:-1]
    msg = msg.replace("'", "")
    msg = msg.replace(",", "")
    message['messages'] = [{"text": u"SCAN RESULT \n " + msg}]
    return message

# print(classify(stock_type='SET100', growth=Decimal(10), lose=Decimal(100), periods=30))
# print(classify(stock_type='SET100', growth=Decimal(7), lose=Decimal(100), periods=60))
# print(classify(stock_type='SET100', growth=Decimal(5), lose=Decimal(100), periods=90))


def main():
    result = gtr.get_growth_stock(stock_type='SET100', growth=Decimal(10), lose=Decimal(100), periods=90)

    X, Y = pepare_data(result)
    # print(X)
    # print(Y)
    slice = int(len(X) * 7 / 10)
    X_train = X[:slice]
    Y_true = Y[len(Y[:slice]):]
    Y = Y[:slice]
    print('PREPARE DATA: TRAIN = ' + str(len(Y)) + '  TEST = ' + str(len(Y_true)))
    print('', Y, '\n', Y_true, '\n')
    X_test = X[len(X_train):]

    # y_train, y_test = fit_predict_LogisticRegression(X_train, Y, X_test)
    # print('LogisticRegression\n', y_train, accuracy_score(Y, y_train), '\n', y_test, accuracy_score(Y_true, y_test))
    # y_train, y_test = fit_predict_AdaBoostClassifier(X_train, Y, X_test)
    # print('AdaBoostClassifier\n', y_train, accuracy_score(Y, y_train), '\n', y_test, accuracy_score(Y_true, y_test))
    y_train, y_test = fit_predict_RandomForestClassifier(X_train, Y, X_test)
    print('RandomForestClassifier\n', y_train, accuracy_score(Y, y_train), '\n', y_test, accuracy_score(Y_true, y_test))
    # y_train, y_test = fit_predict_GradientBoostingClassifier(X_train, Y, X_test)
    # print('GradientBoostingClassifier\n', y_train, accuracy_score(Y, y_train), '\n', y_test,
    #       accuracy_score(Y_true, y_test))
    # y_train, y_test = fit_predict_KNeighborsClassifier(X_train, Y, X_test)
    # print('KNeighborsClassifier\n', y_train, accuracy_score(Y, y_train), '\n', y_test, accuracy_score(Y_true, y_test))
    # y_train, y_test = fit_predict_SVC(X_train, Y, X_test)
    # print('Support Vector Classification\n', y_train, accuracy_score(Y, y_train), '\n', y_test,
    #       accuracy_score(Y_true, y_test))
    # print('\n')
