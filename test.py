# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 11:08:04 2014

@author: wybert
"""
import numpy as np
import datetime
from spyne.model.primitive import Float,Date
from spyne.model.complex import ComplexModel
import cPickle

def weibo_query(date,city,tag):
    if city=='BJ':
        data=np.load('data/BJ_weibo_yuyi_result.npy')
    elif city=='SH':
        data=np.load('data/SH_weibo_yuyi_result.npy')
    elif city=='WH':
        data=np.load('data/WH_weibo_yuyi_result.npy')

    if tag=='good':
        i=1
    elif tag=='bad':
        i=2
        
    for item in data:
        if item[0]==date:
            return item[i]
#
#


###complex data model,weather data

class Weather(ComplexModel):
    
    date=Date
    temperature =Float
    humid =Float
    pressure =Float
    wind_speed =Float
    wind_dir =Float
    Blowing =Float
    Clouds =Float
    Grains =Float
    Sand =Float
    Light =Float
    Clear =Float
    Overcast =Float
    Freezing =Float
    Snow=Float 
    Rain =Float
    Thunderstorm =Float
    Haze =Float
    Fog =Float
    Cloudy =Float
    Showers =Float
    Drizzle =Float
    Dust =Float
    Mist =Float
    Thunderstorms =Float
    RainQ =Float


def query_weather(date,city):
    
    if city=='BJ':
        data=np.load('data/beijingWeather_data_new.npy')
    elif city=='SH':
        data=np.load('data/shanghaiWeather_data_new.npy')
    elif city=='WH':
        data=np.load('data/wuhanWeather_data_new.npy')
    for item in data:
        if item[0]==date:
            return_data = item
    weather={}
    keys=['date','temperature','humid','pressure','wind_speed','wind_dir','Blowing','Clouds',
    'Grains','Sand','Light','Clear','Overcast','Freezing','Snow','Float',
    'Rain','Thunderstorm','Haze','Fog','Cloudy','Showers','Drizzle','Dust',
    'Mist','Thunderstorms','RainQ']
    for i,item in enumerate(return_data):
#        print i,item
        weather[keys[i]]=item

    return Weather(**weather)
#



##define mode predictservice


def modelpredict(date,city,today_weibo_good,today_weibo_bad,
                 yestoday_weibo_good,
                 today_weather,yestoday_weather):
    
    input_data_set={}
    weeknum=[22, 20, 21, 21, 22, 17, 17]
    pop={'BJ':1297.46,'SH':600.93,'WH':90.71}
    aday=datetime.timedelta(days=1)
    input_data_set['good1']=(yestoday_weibo_good/float(weeknum[(date-aday).weekday()]))/pop[city]
    input_data_set['wind_speed1']=yestoday_weather.wind_speed
    input_data_set['wind_dir1']=yestoday_weather.wind_dir
    input_data_set['Rain1']=yestoday_weather.Rain 
    input_data_set['good2']=(today_weibo_good/float(weeknum[date.weekday()]))/pop[city]
    input_data_set['bad2']=(today_weibo_bad/float(weeknum[date.weekday()]))/pop[city]
    input_data_set['temperature2']=today_weather.temperature
    input_data_set['humid2']=today_weather.humid
    input_data_set['pressure2']=today_weather.pressure
    input_data_set['wind_speed2']=today_weather.wind_speed
    input_data_set['wind_dir2']=today_weather.wind_dir
    input_data_set['Rain2']=today_weather.Rain
    input_data_set['Haze2']=today_weather.Haze
    inputdata_list=input_data_set.values()
    print inputdata_list

    trained_machine=cPickle.load(file('machine.pkl','rb'))
    out_data = trained_machine.predict(inputdata_list)
    return out_data[0]
    






aday=datetime.timedelta(days=1)
today=datetime.date(2014,1,3)    
yesterday=today-aday
city='SH'       
today_weibo_good=weibo_query(today,city,'good')
today_weibo_bad=weibo_query(today,city,'bad')
yestoday_weibo_good=weibo_query(yesterday,city,'good')
today_weather= query_weather(today,city)
yestoday_weather=query_weather(yesterday,city)

print modelpredict(today,city,today_weibo_good,today_weibo_bad,
                 yestoday_weibo_good,
                 today_weather,yestoday_weather)






















