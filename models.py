from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC


def fit_predict_LogisticRegression(X_train, Y, X_test):
    m = LogisticRegression()
    m.fit(X_train, Y)
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    return y_train, y_test


def fit_predict_AdaBoostClassifier(X_train, Y, X_test):
    m = AdaBoostClassifier()
    m.fit(X_train, Y)
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    return y_train, y_test


def fit_predict_RandomForestClassifier(X_train, Y, X_test):
    m = RandomForestClassifier()
    m.fit(X_train, Y)
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    return y_train, y_test


def fit_predict_KNeighborsClassifier(X_train, Y, X_test):
    m = KNeighborsClassifier()
    m.fit(X_train, Y)
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    return y_train, y_test


def fit_predict_GradientBoostingClassifier(X_train, Y, X_test):
    m = GradientBoostingClassifier()
    m.fit(X_train, Y)
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    return y_train, y_test


def fit_predict_SVC(X_train, Y, X_test):
    m = SVC()
    m.fit(X_train, Y)
    y_train = m.predict(X_train)
    y_test = m.predict(X_test)
    return y_train, y_test
