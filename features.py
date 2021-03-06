import pandas as pd
from sklearn.preprocessing import MinMaxScaler
import numpy as np
from sklearn.model_selection import train_test_split

def loadDataset(symbol):
    df = pd.read_csv(''+symbol+'.csv', parse_dates=['Date'])
    df = df.set_index('Date') #sets index of the dataframe as the Date column instead of ordinal numbering.
    return df

def splitDataset(X, y):
    '''Splits the data into Training and Test/Dev set. 80% - Train.
    '''
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    return X_train, X_test, y_train, y_test

def addFeatures(df):
    '''Following features have been considered:
    1. High-Low: It is the difference between High and Low prices of a stock for a particular day.
    2. PCT_change: It calculates the percent change shift on 5 days.
    3. MDAV5: It is the Rolling Mean Window calculation for 5 days.
    4. EMA5: Exponential Moving Average for 5 days.
    5. MACD/MACD_SignalLine: Moving Average Convergence/Divergence Oscillator. Difference between EMA26 - EMA12
    6.Return Out: Shifts the Adj. Close for stock prices by 1 day.
    Change: It is the difference between the ReturnOut and Adj. Close for a day.
            Indicates the rise/fall of the stock price for a day wrt the previous day.
    '''
    df['high_low'] = df['high']-df['low']
    df['pct_change'] = df['adj_close'].pct_change(5)
    df['mdav5'] = (df.loc[:,'close']).rolling(window=5).mean()
    df['ema5'] = (df.loc[:, 'close']).ewm(ignore_na=False, min_periods=5, com=5, adjust=True).mean()
    df['ema26'] = (df.loc[:, 'close']).ewm(ignore_na=False, min_periods=26, com=26, adjust=True).mean()
    df['ema12'] = (df.loc[:, 'close']).ewm(ignore_na=False, min_periods=12, com=12, adjust=True).mean()
    df['macd'] = df['ema26'] - df['ema12']
    df['macd_signalline'] = (df.loc[:, 'macd']).ewm(ignore_na=False, min_periods=0, com=9, adjust=True).mean()
    df = df.drop(['ema26', 'ema12'], axis=1)
    #plot.feature_plot(df)
    df['returnout'] = df['adj_close'].shift(-1)
    df = df.dropna()
    df.loc[:, 'change'] = df.loc[:, 'returnout'] - df.loc[:, 'adj_close'] > 0 
    X = df.loc[:, 'adj_close':'macd_signalline']
    y = df.loc[:, 'close']
    return [X, y]

def featureScaling(train, test):
    '''Feature scaler fits on the training set and applies transformation on the train and test set, for uniformity in data.'''
    scaler = MinMaxScaler()
    scaler.fit(train)
    train = scaler.transform(train)
    test = scaler.transform(test)
    return [train, test]