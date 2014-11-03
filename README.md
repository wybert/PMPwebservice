IamJoking
=========

#应用微博以及天气数据估测空气质量状况服务发布

###数据说明

data文件夹里的是胡数据
.npy .pkl形式的都是数据

###源文件使用说明
运行myServey.py就可以发布服务了
有个客户端代码示例：client_test.py

## 在使用git提交的时候出现如下错误
```python
warning: LF will be replaced by CRLF in machine.pkl.
The file will have its original line endings in your working directory.
``` 
训练好的模型被序列化后在传输的过程中可能不够稳定，若服务出现无法运行，请告诉我要machine.pkl原始文件

API说明
========

### 一、空气污染相关微博数据查询服务:query_weibo

**功能：**

实现查询某天某个城市已经处理好的说空气污染好或者坏的数量，北京市数据提供2013年全年，上海、武汉只提供2013年1月份

**定义：** 

`def query_weibo(date,city,tag):`

**输入：** 
- date:datetime 时间
- city:string  输入值为BJ SH WH 之一
- tag:string 值为：good或者bad

**输出：** 
- float 查询到的符合条件的微博数


### 二、气象数据查询服务:query_weather

**功能：** 

实现查询某个城市某天的天气状况，返回一个天气类型weather的数据，数据定义见下面的文档，北京市数据提供2013年全年，上海、武汉只提供2013年1月份

**定义：** 

`def query_weather(date,city)`

**输入：** 
- date:datetime 时间 北京数据提供2013全年的，上海武汉数据提供2014年一月份
- city:string  输入值为BJ SH WH 之一

**输出：** 
- weather数据类型，里面包含当天的天气质量状况信息


### 三、气象数据查询服务:modelpredict

**功能：** 

实现模型估测服务，输入想要估测的城市、日期、以及查询得到的说空气质量好与说空气质量坏的微博数，以及天气状况，来估测当天的空气质量状况

**定义：** 

`def modelpredict(date,city,today_weibo_good,today_weibo_bad,
                     yestoday_weibo_good,
                     today_weather,yestoday_weather)`

**输入：** 
- date:datetime 时间 北京2013全年的，上海武汉2014年一月份
- city:string  输入值为BJ SH WH 之一
- today_weibo_good:float 要估测的当天说空气质量好的微博数
- today_weibo_bad:float 要估测的当天说空气质量坏的微博数
- yestoday_weibo_good:float 要估测的前一天说空气质量好的微博数
- today_weather：weather 要估测的当天天气数据
- yestoday_weather:weather 要估测的前一天天气数据

**输出：** 
- float 估测的当天的空气质量状况值

### 四、weather数据类型

**功能：** 

实现不同气象数据指标的统一管理

**定义：** 
```python
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
```
**数据含义说明：** 
- date Date 日期
- temperature  Float 平均温度
- humid  Float 平均湿度
- pressure  Float 平均气压
- wind_speed  Float 平均风速
- wind_dir  Float 风向，风向值的方差
- Blowing  Float 一天多少小时刮风
- Clouds  Float 一天多少小时多云
- Grains  Float 一天多少小时有颗粒物
- Sand  Float 一天多少小时吹沙
- Light  Float 一天多少小时闪电
- Clear  Float 一天多少小时晴天
- Overcast  Float 一天多少小时阴天
- Freezing  Float 一天多少小时冰冻
- Snow Float 一天多少小时下雪
- Rain  Float 一天多少小时下雨
- Thunderstorm  Float 一天多少小时雷阵雨
- Haze  Float 一天多少小时霾
- Fog  Float 一天多少小时雾
- Cloudy  Float 一天多少小时多云
- Showers  Float 一天多少小时下小雨
- Drizzle  Float 一天多少小时下毛毛雨
- Dust  Float 一天多少小时出现灰尘
- Mist  Float 一天多少小时有雾
- Thunderstorms  Float 一天多少小时雷阵雨
- RainQ  Float 一天下雨量
