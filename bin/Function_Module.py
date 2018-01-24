# -*- coding: utf-8 -*-
import time,os
import numpy as np
import matplotlib.pyplot as plt

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import API_Tushare

def select_by_time(start_time,end_time,stock_basic_data):
    #stock_basic_data = API_Tushare.get_stock_basic(file_time)
    stock_basic_data_list = []
    for index_code in stock_basic_data.index:
        try:
            if time.mktime(time.strptime(str(stock_basic_data.loc[index_code]['timeToMarket']), '%Y%m%d')) >= time.mktime(time.strptime(start_time, '%Y%m%d')):
                if time.mktime(
                        time.strptime(str(stock_basic_data.loc[index_code]['timeToMarket']), '%Y%m%d')) <= time.mktime(
                        time.strptime(end_time, '%Y%m%d')):
                    stock_basic_data_list.append(index_code)
        except:
            pass
    return stock_basic_data_list

def select_by_code(code_list,stock_basic_data):
    #stock_basic_data = API_Tushare.get_stock_basic(file_time)
    stock_basic_data_list = []
    for index_code in stock_basic_data.index:
        for code_item in code_list:
            if stock_basic_data.loc[index_code]['ncode']==code_item:
                stock_basic_data_list.append(index_code)

    return stock_basic_data_list



def create_image_2(code_list,h_point_day_list,net_profits_list):
    fig,ax = plt.subplots()
    index = np.arange(len(code_list))
    bar_width = 0.35
    opacity = 0.4

    rects1 = ax.bar(index, net_profits_list, bar_width,alpha=opacity, color='b',label='net_profits')
    rects2 = ax.bar(index + bar_width, h_point_day_list, bar_width,alpha=opacity, color='r',label='h_point_day')

    ax.set_xlabel('Group')
    ax.set_ylabel('Scores')
    ax.set_title('Scores by group and gender')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(code_list,rotation=90, fontsize=10)
    ax.legend()
    fig.tight_layout()
    plt.show()



def create_image(stock_basic_data_item,price_list,select_index_item,filename,file_time):

    list_price = []
    list_time  = []
    select_list_price = []
    select_list_time  = []

    for index_itme in price_list.index:
        try:
            list_price.append(price_list[index_itme])
            list_time.append(index_itme.strftime("%Y-%m-%d"))
        except:
            list_time.append(index_itme)
    for index_itme in select_index_item:
        try:
            select_list_price.append(price_list[index_itme])
            select_list_time.append(list_time.index(index_itme.strftime("%Y-%m-%d")))
        except:
            select_list_time.append(list_time.index(index_itme))



    p = len(list_time)/60
    if p == 0:
        p = 1
    xticks = range(0, len(list_time), p)
    xticklabels = []
    for i in xticks:
        xticklabels.append(list_time[i])

    fig = plt.figure()
    ax = fig.add_subplot(1,1,1)
    ax.plot(range(0, len(list_time), 1), list_price)
    ax.plot(select_list_time, select_list_price,'or')
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticklabels,rotation=90, fontsize=5)
    #ax.set_xticklabels(xticks, rotation=90, fontsize=5)
    ax.grid(True, linestyle="-", color="r", linewidth="0.5")

    title = '%s pe:%s totals:%s totalAssets:%s esp:%s dp:%s timeToMarket:%s profit:%s gpr:%s npr:%s'%(
                    stock_basic_data_item['ncode'],
                    stock_basic_data_item['pe'],
                    stock_basic_data_item['totals'],
                    stock_basic_data_item['totalAssets'],
                    stock_basic_data_item['esp'],
                    stock_basic_data_item['pb'],
                    stock_basic_data_item['timeToMarket'],
                    stock_basic_data_item['profit'],
                    stock_basic_data_item['gpr'],
                    stock_basic_data_item['npr'],)
    plt.title(title,fontsize=5)
    # plt.show()

    dirname = os.path.dirname(os.path.realpath(__file__))
    image = dirname + os.path.sep + ".." + os.path.sep + 'stock_market_data'+ os.path.sep +'image_result' + os.path.sep + '%s%s%s.png' % (file_time,filename,stock_basic_data_item['ncode'])

    #fig.autofmt_xdate()
    #plt.show()

    plt.savefig(image,dpi=200)
    plt.close()
    #input("input:")


# find low point
# item = [date,open,high,close,low,volume,price_change,p_change,ma5,ma10,ma20,v_ma5,v_ma10,v_ma20,turnover]
# point = low ,high
def function_1(pa_stock_price_data,item,times):

    index_list = pa_stock_price_data.index
    price_select = []
    for index_item in index_list:
        if pa_stock_price_data.loc[index_item][item]!='':
            try:
                if pa_stock_price_data.loc[index_item][item] != pa_stock_price_data.loc[price_select[-1]][item]:
                    price_select.append(index_item)
            except:
                price_select.append(index_item)

    index_list = price_select

    while(True):
        price_select = []
        price_list_3 = []

        price_list_3.append(float(pa_stock_price_data.loc[index_list[0]][item]))
        price_list_3.append(float(pa_stock_price_data.loc[index_list[1]][item]))
        price_list_3.append(float(pa_stock_price_data.loc[index_list[2]][item]))


        if price_list_3[0]<price_list_3[1]:
            price_select.append(index_list[0])
        elif price_list_3[0]>price_list_3[1] and price_list_3[1]<price_list_3[2]:
            price_select.append(index_list[1])


        for i in range(3,len(index_list),1):
            price_list_3.pop(0)
            price_list_3.append(float(pa_stock_price_data.loc[index_list[i]][item]))

            if i == (len(index_list)-1):
                if price_list_3[1] > price_list_3[2]:
                    price_select.append(index_list[i])

            if price_list_3[0] > price_list_3[1] and price_list_3[1] < price_list_3[2]:
                #print price_list_3[0],price_list_3[1],price_list_3[2]
                price_select.append(index_list[i-1])

        #print '*****************************'
        if len(price_select) <= times:
            #print len(price_select)
            return price_select
        else:
            index_list = price_select
            #print len(index_list)
# return : price _select =[index_item,....]

# find high point between two low point
def find_high_point_between_two_point(low_price_select_list,pa_stock_price_data,item):
    point_1 = low_price_select_list[0]

    high_price_select_list = []
    for i in range(1, len(low_price_select_list), 1):
        point_2 = low_price_select_list[i]
        high_price_select_list.append(pa_stock_price_data.loc[point_1:point_2, [item]].sort_values(by=[item],ascending=False).index[0])
        point_1 = low_price_select_list[i]

    return high_price_select_list
    # high_price_select_list = [index_time,....]   #index_time='2017-01-01'


# find first high point and days
def find_first_high_point(pa_stock_price_data,item):
    index_list = pa_stock_price_data.index
    p_price = 0
    i = -1
    for index_item in index_list:
        i = i+1
        if float(pa_stock_price_data.loc[index_item][item])<p_price:
            # return index_item(2017-01-01) and days
            return index_list[i-1], i,p_price
        else:
            p_price = float(pa_stock_price_data.loc[index_item][item])


def find_high_point(pa_stock_price_data,item):
    index_list = pa_stock_price_data.index
    h_price_item = index_list[0]
    day = 0
    i = 0
    for index_item in index_list:
        i = i + 1
        if float(pa_stock_price_data.loc[index_item][item]) > float(pa_stock_price_data.loc[h_price_item][item]):
            h_price_item = index_item
            day = i
    # return index_item(2017-01-01) and days
    return h_price_item ,day,float(pa_stock_price_data.loc[h_price_item][item])


# find low point between two high point
def find_low_point_between_two_point(high_price_select_list,pa_stock_price_data,item):
    point_1 = high_price_select_list[0]

    low_price_select_list = []
    for i in range(1, len(high_price_select_list), 1):
        point_2 = high_price_select_list[i]
        low_price_select_list.append(pa_stock_price_data.loc[point_1:point_2, [item]].sort_values(by=[item],ascending=True).index[0])
        point_1 = high_price_select_list[i]

    return low_price_select_list
    # low_price_select_list = [index_time,....]   #index_time='2017-01-01'


