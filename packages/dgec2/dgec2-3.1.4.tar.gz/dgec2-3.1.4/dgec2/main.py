"""
Created on 2023/3/16
@author: Y.C.Huang
数字经济包，用于数字经济测度的计算
"""

import pandas as pd

'''获取数据'''
def db_out():
    data = pd.read_excel(r'databa.xlsx') 
    print("data installed!")
    return data

'''输出年份'''
def db_year(data,year):
    try:
        if year<2020 or year>2027:
            print("accepted year must between 2020 and 2027!")
            return 
        db_year = data[data['年']==year]
        print("input year "+str(year))
        print(db_year)
        return db_year
    except:
        print("error! data uncorrect!")
        return

'''输出城市'''
def db_city(data,city):
    try:
        db_city = data[['年',str(city)]]
        print("input city "+str(city))
        print(db_city)
        return db_city
    except:
        print("error! data uncorrect!")
        return

'''dataframe 转 list'''
def tolist(data):
    return data.values.tolist()



