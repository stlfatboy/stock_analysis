# -*- coding: utf-8 -*-
#https://query1.finance.yahoo.com/v7/finance/download/600352?period1=915120000&period2=1515046167&interval=1d&events=history&crumb=eQnub0LqdHP
#https://query1.finance.yahoo.com/v7/finance/download/600352.SS?period1=1512368342&period2=1515046742&interval=1d&events=history&crumb=eQnub0LqdHP



import sys
reload(sys)
sys.setdefaultencoding('utf8')



import xlrd
import requests
import pandas_datareader.data as web
import datetime, os,json
import pandas
import csv
import tushare
import numpy as np

import API_Tushare, Function_Module
import time,datetime






def main_funciton_1(select_index_list,pa_stock_basic_data):

    for stock_basic_data_index_item_code in select_index_list:

        # pa_stock_price_data = [date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover]
        pa_stock_price_data = API_Tushare.get_one_stock_price_save_csv_from_tushare(pa_stock_basic_data.loc[stock_basic_data_index_item_code]['ncode'], file_time)

        #pa_stock_price_data = API_Tushare.get_one_stock_price_save_csv_from_yahoo(pa_stock_basic_data.loc[stock_basic_data_index_item_code]['ncode'], file_time)

        select_index_item = Function_Module.function_1(pa_stock_price_data, 'low', 50)
        high_price_select_list = Function_Module.find_high_point_between_two_point(select_index_item,pa_stock_price_data,'low')
        select_index_item.extend(high_price_select_list)

        h_point, days = Function_Module.find_first_high_point(pa_stock_price_data,'low')
        select_index_item.append(h_point)

        stock_report_data = API_Tushare.get_stock_report_data(2017, 3)
        close_price_list = pa_stock_price_data.xs('low', axis=1)
        Function_Module.create_image(pa_stock_basic_data.loc[stock_basic_data_index_item_code],close_price_list,select_index_item)


def main_function_2(select_index_list,pa_stock_basic_data,stock_report_data):

    code_list = []
    h_point_day_list = []
    net_profits_list = []



    for stock_basic_data_index_item_code in select_index_list:
        pa_stock_price_data = API_Tushare.get_one_stock_price_save_csv_from_tushare(
            pa_stock_basic_data.loc[stock_basic_data_index_item_code]['ncode'], file_time)

        h_point, days = Function_Module.find_first_high_point(pa_stock_price_data, 'low')

        try:
            net_profits_list.append(float(stock_report_data[pa_stock_basic_data.loc[stock_basic_data_index_item_code]['ncode']]['net_profits']))
            code_list.append( pa_stock_basic_data.loc[stock_basic_data_index_item_code]['ncode'])
            h_point_day_list.append(days*1000)

        except:
            pass

    print len(code_list),len(h_point_day_list),len(net_profits_list)
    Function_Module.create_image_2(code_list,h_point_day_list,net_profits_list)




def main_function_3(select_index_list,pa_stock_basic_data,stock_report_data,file_time):


    select_data_dict_seq = ['code',
                            'name',
                            'industry',
                            'area',
                            'net_profits',
                            'profits_yoy',
                            'pe',
                            'totals',
                            'esp',
                            'timeToMarket',
                            'Frist_price',
                            'Frist_high_day',
                            'Frist_high_price',
                            'low_bet_fh_h_day',
                            'low_price_bet_fh_h_price',
                            'high_day',
                            'high/low_price',
                            'high/FH',
                            'ma20/FH']

    select_data_dict = dict.fromkeys(select_data_dict_seq)
    for key in select_data_dict.keys():
        select_data_dict[key] = []

    #print select_data_dict
    ii = 0
    file_name = '2017_all_new_stock'
    for stock_basic_data_index_item_code in select_index_list:
        try:
            pa_stock_basic_data_item = pa_stock_basic_data.loc[stock_basic_data_index_item_code]
            pa_stock_price_data = API_Tushare.get_one_stock_price_save_csv_from_tushare(pa_stock_basic_data_item['ncode'], file_time)
            fh_point_time_item, fh_days, fh_price = Function_Module.find_first_high_point(pa_stock_price_data, 'low')
            h_point_time_item, h_days, h_price    = Function_Module.find_high_point(pa_stock_price_data, 'low')
            l_point_between_fh_h_time_item_list   = Function_Module.find_low_point_between_two_point([fh_point_time_item, h_point_time_item], pa_stock_price_data, 'low')

        except:
            continue
        aaa =1
        if aaa == 1:#(h_days>fh_days):#and (pa_stock_price_data.loc[pa_stock_price_data.index[-1]]['ma20']>fh_price):

            select_index_item = Function_Module.function_1(pa_stock_price_data, 'low', 10)
            high_price_select_list = Function_Module.find_high_point_between_two_point(select_index_item, pa_stock_price_data, 'low')
            select_index_item.extend(high_price_select_list)
            select_index_item.append(fh_point_time_item)

            # create image
            #Function_Module.create_image(pa_stock_basic_data_item, pa_stock_price_data.xs('low', axis=1), select_index_item, file_name, file_time)
            try:
                select_data_dict['net_profits'].append(stock_report_data[pa_stock_basic_data_item['ncode']]['net_profits'])
                select_data_dict['profits_yoy'].append(stock_report_data[pa_stock_basic_data_item['ncode']]['profits_yoy'])

                select_data_dict['code'    ].append(pa_stock_basic_data_item['ncode'])
                select_data_dict['name'    ].append(pa_stock_basic_data_item['name'])
                select_data_dict['industry'].append(pa_stock_basic_data_item['industry'])
                select_data_dict['area'    ].append(pa_stock_basic_data_item['area'])
                select_data_dict['pe'      ].append(pa_stock_basic_data_item['pe'])
                select_data_dict['totals'  ].append(pa_stock_basic_data_item['totals'])
                select_data_dict['esp'     ].append(pa_stock_basic_data_item['esp'])

                # first price point
                select_data_dict['timeToMarket'].append(pa_stock_basic_data_item['timeToMarket'])
                select_data_dict['Frist_price' ].append(pa_stock_price_data.loc[pa_stock_price_data.index[0]]['low'])

                #first high price point
                select_data_dict['Frist_high_day'  ].append(fh_days)
                select_data_dict['Frist_high_price'].append((fh_price - select_data_dict['Frist_price' ][-1]) / select_data_dict['Frist_price' ][-1])

                #low price point between fh and h
                select_data_dict['low_bet_fh_h_day'  ].append(l_point_between_fh_h_time_item_list[0] - fh_point_time_item)
                select_data_dict['low_price_bet_fh_h_price'].append((-fh_price + pa_stock_price_data.loc[l_point_between_fh_h_time_item_list[0]]['low']) / fh_price)

                #high pirce point
                select_data_dict['high_day'].append(h_point_time_item - l_point_between_fh_h_time_item_list[0])
                select_data_dict['high/low_price'].append((h_price - pa_stock_price_data.loc[l_point_between_fh_h_time_item_list[0]]['low'])/ pa_stock_price_data.loc[l_point_between_fh_h_time_item_list[0]]['low'])
                select_data_dict['high/FH'].append((h_price - fh_price) / fh_price)

                #last point
                select_data_dict['ma20/FH'].append((pa_stock_price_data.loc[pa_stock_price_data.index[-1]]['ma20'] - fh_price) / fh_price)

            except:
                print 'error',ii,pa_stock_basic_data_item['ncode']
                ii = ii+1

    pandas_data = pandas.DataFrame()
    i = 0
    for key in select_data_dict_seq:
        pandas_data.insert(i,key,select_data_dict[key])
        i = i+1

    dirname = os.path.dirname(os.path.realpath(__file__))
    filename = dirname + os.path.sep + ".." + os.path.sep + "stock_market_data" + os.path.sep + '%s.csv'%file_name
    pandas_data.to_csv(filename,encoding="utf_8_sig")









if __name__ == '__main__':
    #function_5()
    start_time = '20170101'
    end_time   = '20171231'
    file_time  = '20180124'

    #get basic data
    pa_stock_basic_data = API_Tushare.get_stock_basic(file_time)
    stock_report_data = API_Tushare.get_stock_report_data(2017, 3)

    # select_list is pa_stock_basic_data's index ...['603027','603955','603903','603139','603320']
    select_index_list = Function_Module.select_by_time(start_time, end_time,pa_stock_basic_data)
    #select_index_list = Function_Module.select_by_code(['002865'],file_time)


    #main_function_2(select_index_list, pa_stock_basic_data, stock_report_data)
    main_function_3(select_index_list,pa_stock_basic_data,stock_report_data,file_time)






























