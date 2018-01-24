# -*- coding: utf-8 -*-

import tushare,pandas
import os,datetime
import pandas_datareader.data as web









#input t_time = '2018-01-01'
#read local file first, if no download file
def get_stock_basic(file_time):

    dirname = os.path.dirname(os.path.realpath(__file__))
    filename = dirname + os.path.sep + ".."+ os.path.sep + "stock_market_data" + os.path.sep + 'stock_basic_%s.csv'%file_time
    try:
        data = pandas.DataFrame.from_csv(filename)
    except:
        data = tushare.get_stock_basics()
        data = data.sort_values(by=['timeToMarket'])
        data.to_csv(filename,encoding="utf_8_sig")

    ncode = []
    for index_code in data.index:
        code = str(index_code)
        for i in range(0, (6 - len(code)), 1):
            code = '0%s' % code
        ncode.append(code)
    data.insert(0, 'ncode', ncode)

    return data
#code,ncode,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket,undp,perundp,rev,profit,gpr,npr,holders
# return pandas file



#input t_time = '2018-01-01'
#read local file first, if no download file
def get_stock_report_data(year,s):

    dirname = os.path.dirname(os.path.realpath(__file__))
    filename = dirname + os.path.sep + ".."+ os.path.sep + "stock_market_data" + os.path.sep + 'stock_report_data_%s_%s.csv'%(year,s)
    try:
        data = pandas.DataFrame.from_csv(filename)
    except:
        data = tushare.get_report_data(year,s)
        data.to_csv(filename,encoding="utf_8_sig")

    # can use DataFrame.set_index
    new_data={}
    for item in data.index:
        temp_data = data.loc[item]

        code = str(temp_data['code'])
        for i in range(0, (6 - len(code)), 1):
            code = '0%s' % code
        new_data[code] = temp_data
        #print type(temp_data['code']),temp_data['code']
    return new_data
#code,ncode,name,industry,area,pe,outstanding,totals,totalAssets,liquidAssets,fixedAssets,reserved,reservedPerShare,esp,bvps,pb,timeToMarket,undp,perundp,rev,profit,gpr,npr,holders
# return pandas file


def get_one_stock_price_save_csv_from_tushare(code,file_time):

    dirname = os.path.dirname(os.path.realpath(__file__))
    filename = dirname + os.path.sep + ".." + os.path.sep + "stock_market_data"+ os.path.sep + "stock_data_from_tushare" + os.path.sep + '%s_%s.csv' %(code,file_time)
    try:
        data = pandas.DataFrame.from_csv(filename)
    except:
        data = tushare.get_hist_data(code,start='2007-03-01',end='2018-01-16')
        data = data.sort_index(axis=0, ascending=True)
        data.to_csv(filename,encoding="utf_8_sig")

    return data



def get_one_stock_price_save_csv_from_yahoo(code,file_time):
    start = datetime.datetime(1980, 1, 1)
    end = datetime.datetime(2017, 12, 31)
    dirname = os.path.dirname(os.path.realpath(__file__))
    filename = dirname + os.path.sep + ".." + os.path.sep + "stock_market_data" + os.path.sep + "stock_data_from_yahoo" + os.path.sep + 'yahoo_%s_%s.csv' % (code, file_time)

    try:
        data = pandas.DataFrame.from_csv(filename)
    except:
        try:
            code_ss = '%s.ss' % int(code)
            data = web.DataReader(code_ss, 'yahoo', start, end)
        except:
            data = web.DataReader(str(int(code)), 'yahoo', start, end)

        data = data.sort_index(axis=0, ascending=True)
        data.to_csv(filename,encoding="utf_8_sig")
    return data


