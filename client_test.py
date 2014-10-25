# -*- coding: utf-8 -*-
"""
Created on Tue Sep 23 09:45:55 2014

@author: wybert
"""
import suds
import numpy as np
import datetime

# url=u'http://172.23.77.1:8000/?wsdl'
# c=suds.client.Client(url)



# SH_DataSet=np.load('SH_DataSet.npy')

# Data,Target=SH_DataSet[:,1:-1],SH_DataSet[:,-1] 
# input_test=Data[1,:]
# #
# #input_test = input_test.astype(np.int)

# input_test=list(input_test)

# #print c.service.predict(input_test)

# test = c.factory.create('floatArray')
# test.float=input_test
# print c.service.predict(test)
url=u'http://localhost:8000/?wsdl'
c=suds.client.Client(url)
print c
# date=datetime.date(2014,1,3)
# city='SH'
# tag='bad'

# print c.service.weibo_query(date,city,tag)
# print c.service.query_weather(date,city)
# print c.service.query_weather


aday=datetime.timedelta(days=1)
today=datetime.date(2014,1,3)    
yesterday=today-aday
city='SH'       
today_weibo_good=c.service.weibo_query(today,city,'good')
today_weibo_bad=c.service.weibo_query(today,city,'bad')
yestoday_weibo_good=c.service.weibo_query(yesterday,city,'good')
today_weather= c.service.query_weather(today,city)
yestoday_weather=c.service.query_weather(yesterday,city)

print c.service.modelpredict(today,city,today_weibo_good,today_weibo_bad,
                 yestoday_weibo_good,
                 today_weather,yestoday_weather)



