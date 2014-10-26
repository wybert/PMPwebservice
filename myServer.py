# -*- coding: utf-8 -*-
"""
Created on Mon Sep 15 12:27:45 2014

@author: zqh
"""

import logging
logging.basicConfig(level=logging.DEBUG)
from spyne.application import Application
from spyne.decorator import rpc
from spyne.service import ServiceBase
#from spyne.model.primitive import Integer
from spyne.model.primitive import Float
from spyne.model.primitive import Date,Unicode
from spyne.model.complex import Iterable
from spyne.protocol.soap import Soap11
from spyne.server.wsgi import WsgiApplication

#from spyne.model.complex import Array
import numpy as np
import cPickle
import datetime
from spyne.model.complex import ComplexModel

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

class modelPredictService(ServiceBase):

    @rpc(Date,Unicode,Unicode,_returns=Float)
    def query_weibo(ctx,date,city,tag):
        if city==u'BJ':
            data=np.load('data/BJ_weibo_yuyi_result.npy')
        elif city==u'SH':
            data=np.load('data/SH_weibo_yuyi_result.npy')
        elif city==u'WH':
            data=np.load('data/WH_weibo_yuyi_result.npy')

        if tag==u'good':
            i=1
        elif tag==u'bad':
            i=2
            
        for item in data:
            if item[0]==date:
                return item[i]

    @rpc(Date,Unicode,_returns=Weather)            
    def query_weather(ctx,date,city):
        
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
        keys=[u'date',u'temperature',u'humid',u'pressure',u'wind_speed',u'wind_dir',u'Blowing',u'Clouds',
        u'Grains',u'Sand',u'Light',u'Clear',u'Overcast',u'Freezing',u'Snow',u'Float',
        u'Rain',u'Thunderstorm',u'Haze',u'Fog',u'Cloudy',u'Showers',u'Drizzle',u'Dust',
        u'Mist',u'Thunderstorms',u'RainQ']
        for i,item in enumerate(return_data):
    #        print i,item
            weather[keys[i]]=item

        return Weather(**weather)

    @rpc(Date,Unicode,Float,Float,Float,Weather,Weather,_returns=Float)
    def modelpredict(ctx,date,city,today_weibo_good,today_weibo_bad,
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
        trained_machine=cPickle.load(file('machine.pkl','rb'))
        out_data = trained_machine.predict(inputdata_list)
        return out_data[0]
   
        
application = Application([modelPredictService],
    tns='spyne.myapp.modelpredict',
    in_protocol=Soap11(validator='lxml'),
    out_protocol=Soap11()
)
if __name__ == '__main__':
    # You can use any Wsgi server. Here, we chose
    # Python's built-in wsgi server but you're not
    # supposed to use it in production.
    from wsgiref.simple_server import make_server
    wsgi_app = WsgiApplication(application)
    server = make_server('0.0.0.0', 8000, wsgi_app)
#    server=make_server(' 172.23.77.1',8000,wsgi_app)
    server.serve_forever()
