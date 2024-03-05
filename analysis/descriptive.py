import pandas as pd
import csv
import os
import numpy as np

def readcsv(filename):
    """
    Read csv for concat purpose
    """
    l = []

    path = os.path.abspath(os.curdir) + '/data/' + filename + '.csv'
    return pd.read_csv(path, na_values=np.nan)

# def __drop_missingvalues(df):

def __print_describe(df_list):
    for i in df_list:
        print(i.describe())

def __print_missing_values(df_list):
    for i in df_list:
        print(i.isnull().sum())


if __name__ == '__main__':

    """
    DATA IMPORT #1.0.0
    """
    # run and preprocessing
    _click_log = readcsv('_click_log')
    _products = readcsv('_products')
    _purchase_log = readcsv('_purchase_log')
    _users = readcsv('_users')

    # descriptive
    __print_describe([_click_log, _products, _purchase_log, _users])

    # missing number
    __print_missing_values([_click_log, _products, _purchase_log, _users])

    """
    USER DEMOGRAPHY #1.1.0
    """
    _pivot_user_count = pd.pivot_table(
        _users,
        index=['age_range'],
        columns=['gender'],
        values=['user_id'],
        aggfunc='count',
    )
    _pivot_user_age_count = pd.pivot_table(
        _users,
        index=['age_range'],
        values=['user_id'],
        aggfunc='count'
    )
    _pivot_user_age_count['% of Total'] = round(
        _pivot_user_age_count.user_id / _pivot_user_age_count.user_id.sum() * 100
    ).astype(str) + '%'

    