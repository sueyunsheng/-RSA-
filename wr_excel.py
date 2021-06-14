import pandas as pd
from pandas import DataFrame

file_path = r'./users.xls'


def read_from_users(uid):
    df = pd.read_excel(file_path, sheet_name=0)
    for i in range(df.shape[0]):
        if uid == df.iloc[i, 0]:
            return True
    return False


def read_users(uid):
    df = pd.read_excel(file_path, sheet_name=0)
    for i in range(df.shape[0]):
        if uid == df.iloc[i, 0]:
            return df.iloc[i, 1], df.iloc[i, 2], df.iloc[i, 3], df.iloc[i, 4]


def wr_to_users(data):
    df = pd.read_excel(file_path)
    df.loc[df.shape[0] + 1] = data
    DataFrame(df).to_excel(file_path, index=False, header=True)


def wr_N(uid, N):
    df = pd.read_excel(file_path, sheet_name=0)
    for i in range(df.shape[0]):
        if uid == df.iloc[i, 0]:
            df.loc[i, 'N'] = N
            DataFrame(df).to_excel(file_path, index=False, header=True)
            break


def wr_to_pwd(uid, pwd):
    df = pd.read_excel(file_path, sheet_name=0)
    for i in range(df.shape[0]):
        if uid == df.iloc[i, 0]:
            df.loc[i, 'password'] = pwd
            DataFrame(df).to_excel(file_path, index=False, header=True)
            break

