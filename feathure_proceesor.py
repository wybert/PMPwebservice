# -*- coding: utf-8 -*-
"""
Created on Mon Oct 20 21:24:18 2014

@author: wybert
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Apr 03 19:02:51 2014

@author: zqh
"""

import numpy as np
import datetime
import csv


def normlize_data(mergered_data,week_num,poplation):

# cosider poplation
    mergered_data[:,[1,2]] = mergered_data[:,[1,2]]/poplation

# consider weekdays
    for item in mergered_data:
        for i in range(7):
            if item[0].weekday()==i:
                item[1]=item[1]/float(week_num[i])
                item[2]=item[2]/float(week_num[i])
            
    return mergered_data
    
    
    
def merger_data(Weather_data_new,weibo_yuyi_result,index):

    Weather_data_new = np.array(Weather_data_new)
    Weather_data_new = Weather_data_new[:,1:]    
 
    weibo_yuyi_result=np.array(weibo_yuyi_result)
    weibo_yuyi=weibo_yuyi_result
#    ---------------------------折叠  ---------------------- 
    data=np.hstack((weibo_yuyi,Weather_data_new))    
#----------------------target----------------------------- 
    target = index[:,1:]
    dataSet_Write_to_R=np.hstack((data,target))
    
    return dataSet_Write_to_R

def featureSlect(mergered_data):


    date_item = ['time']
    weibo_yuyi_item=['good','bad','other']
#    kouzhao_num_item =['KZ_good','KZ_bad','KZ_other']   
    target_item=['target']
    weather_item_new = WEATHER_ITEM_NAME_NEW[1:] 
       
#    item_name = wealth_item + weibo_yuyi_item + kouzhao_num_item+ hp_item+ weather_item_new+target_item
    
#    item_name = wealth_item + weibo_yuyi_item + hp_item+ target_item  

    item_name =  date_item+ weibo_yuyi_item  +  weather_item_new+ target_item
    
    item_name = np.array(item_name)
    
    print "##############################################"

    for i,item in enumerate(item_name) :
        print i,item

    print "##############################################"
    
    
    
    
    fetrue_select_num = range(len(item_name))
    fetrue_select_num = [0,1,2,4,5,6,7,8,9,18,19,20,21,23,24,25,26,27,28,29]

    global SELECTED_FETURE_NAME
    SELECTED_FETURE_NAME = item_name[fetrue_select_num]
    
    print "selected feture set:"
    print "##############################################"

    for i,item in enumerate(SELECTED_FETURE_NAME) :
        print i,item

    print "##############################################"
#    print fetrue_select_num
#    print mergered_data.shape

    fetureSelected_dataSet = mergered_data[:,fetrue_select_num]

    return fetureSelected_dataSet



def featureSelect2(data,N):
    
    
#    define select here 
#    
#    twoDaysAgo=range(1,17)
    oneDaysAgo=[1]
#    today=range(1,28) 
#    
    
    
#    twoDaysAgo=[1,6,7,9,18]
    oneDaysAgo=[1,6,7,9]
    today=[1,2,3,4,5,6,7,9,11,19]


#    define predict fuc
#    twoDaysAgo=[1,6,7,9,18]
#    oneDaysAgo=[1,2,3,4,5,6,7,9,11,18]
#    today=[19]
    
#    today=[2,18]
    ##test
#    oneDaysAgo=[1,6,7]
#    today=[1,2,3,4,5,6,7,9,19]


#    today=[1,2,19]


    Le = len(SELECTED_FETURE_NAME)-1
    
    if N ==1:
        fetrue_select_num =[0]+today
    elif N==2:
        today=[i+Le for i in today]            
        fetrue_select_num=[0]+oneDaysAgo+today        
    elif N==3:
        oneDaysAgo=[i+Le for i in oneDaysAgo]
        today=[i+Le*2 for i in today]            
        fetrue_select_num= [0]+twoDaysAgo+oneDaysAgo+today
    else:
        print 'not coside N>3!!!!!!!'
        
    print fetrue_select_num
    data=np.array(data)
    print "----------------------------------------------"
    print "feture select 2:"
    print "----------------------------------------------"
    print "total feture here:"
    for i,item in enumerate(SELECTED_FETURE_NAME_consider_BD):
        print i,item
        
    print "---------------------------------------------"

    print "selected feture here:"
    for i,item in enumerate(SELECTED_FETURE_NAME_consider_BD[fetrue_select_num]):
        print i,item
    print "--------------------------------------------"
    global  SELECTED_FETURE_NAME_FINAL
    
    SELECTED_FETURE_NAME_FINAL = SELECTED_FETURE_NAME_consider_BD[fetrue_select_num]
    finaldataset=data[:,fetrue_select_num]

    return finaldataset





def resample(fetureSelected_dataSet,day_loss):
    
# conside time factor
    dataSet_filter_by_time = [item for item in fetureSelected_dataSet if 
#               (item[0] <=dateEnd or (item[0] >=dateStart)) and
            item[0] not in day_loss
#                and ( item[19]>=0 and item[19] <= 500)               
           ]
    dataSet_filter_by_time = np.array(dataSet_filter_by_time)
    

    
    startDate = np.min(dataSet_filter_by_time[:,0])
    endDate = np.max(dataSet_filter_by_time[:,0])
    aDay=datetime.timedelta(days = 1)
    i=0
    loseyuhao=[]
    flag =0
    endflag=len(dataSet_filter_by_time)
#    print endflag,'$_$'
    while startDate <= endDate:
        if dataSet_filter_by_time[i,0] ==startDate:
            tail=dataSet_filter_by_time[flag:endflag+1,:]
                     
        else:
            
            if i != flag:
                loseyuhao.append(dataSet_filter_by_time[flag:i,:])
#                print i,'#_#',dataSet_filter_by_time[i,0],startDate            
            flag = i
            i-=1
                                    
        i+=1
        startDate += aDay
    loseyuhao.append(tail)
#    print loseyuhao

    checkuse=0
    for item in loseyuhao:
        checkuse+= len(item)
    if checkuse != endflag:
        print '@_@'
        
    
    
    
    return loseyuhao



def resample_cosider_before_days(resampled_data,N):

    
#    N=1
    global SELECTED_FETURE_NAME_consider_BD
    SELECTED_FETURE_NAME_consider_BD=[]
    for i in range(1,N+1):
        for item in SELECTED_FETURE_NAME[1:]:
            SELECTED_FETURE_NAME_consider_BD.append(item+str(i))
    SELECTED_FETURE_NAME_consider_BD = [u'time']+SELECTED_FETURE_NAME_consider_BD    
    SELECTED_FETURE_NAME_consider_BD = np.array(SELECTED_FETURE_NAME_consider_BD)
    
    
    date = resampled_data[:,0]
    date = date[N-1:]
    
    resampled_data_not_contain_time=resampled_data[:,1:]
#    print resampled_data[:,1:]

    num_Sample = len(resampled_data_not_contain_time)-N+1
    dataSet = []
    for i in range(num_Sample):
        
        temp = resampled_data_not_contain_time[i:i+N,:]
        temp.ravel()
        oneSample=[]
        for item in temp:
            oneSample += list(item)
        

#        print temp
#        break
        dataSet += [oneSample]
        
    dataSet = np.array(dataSet)
    

#    date =np.zeros((len(dataSet),1))
    date=np.array(date)
#    print date.shape
    date = date.reshape((len(dataSet),1))
#    print date.shape
#    print dataSet.shape

#    print date
    dataSet = np.hstack((date,dataSet))

    return dataSet


 

def loadDataSet(Weather_data_new,
                weibo_yuyi_result,Index,
                week_num,day_loss,poplation):
    

#    target=transIndex2Levels(Index)
    mergered_data = merger_data(Weather_data_new,
                                weibo_yuyi_result,Index)
    
#    saveData_view(mergered_data,'mergered_data')
    
    normlized_data = normlize_data(mergered_data,week_num,poplation) 
    
#    saveData_view(normlized_data,'normlized_data')
    
    featureSlected_data = featureSlect(normlized_data) 
    
#    saveData_view(featureSlected_data,'featureSlected_data')
    
    resampled_data2 =  resample(featureSlected_data,day_loss)
    
#    saveData_view(resampled_data,'resampled_data')
    
    resampled_cosider_before_days=[]
    N=2
    
    for item in resampled_data2:
#        print resampled_data2
        
        resampled_cosider_before_days += list(resample_cosider_before_days(item,N))
    
#    print "^&*",len(resampled_cosider_before_days)
    
    featureSlected_data2 = featureSelect2(resampled_cosider_before_days,N)

    
    
    return featureSlected_data2
  
def saveData_view(data,filename):

    item_name = SELECTED_FETURE_NAME_FINAL
  
    
    with open(filename+'_wirite.csv','wb') as csvfile:
        swriter=csv.writer(csvfile,delimiter=',',quotechar=',', quoting=csv.QUOTE_MINIMAL)
        swriter.writerow(item_name)
        for item in data:
            swriter.writerow(item)        
    

if __name__ == '__main__':
    
    beijing_pop=1297.46
    
#    some test here blow
#    beijing_pop=25876
    day_loss =set()
    BJ_DataSet = loadDataSet(beijingWeather_data_new,
                             BJ_weibo_yuyi_result,
                             BJ_Index,
                             week_num,day_loss,beijing_pop)


#    xiamen_pop=190.92
#    XM_DataSet = loadDataSet(XM_Weather,XMKQWR_yuyiResult,XM_KZ_NUM,XM_Index,week_num,predict_dayloss,xiamen_pop)
#    
#    shanghai_pop=1426.93
    shanghai_pop=600.93    
#    #    some test here blow
#    shanghai_pop=3354
#
    predict_dayloss =set()
    SH_DataSet = loadDataSet(shanghaiWeather_data_new,
                             SH_weibo_yuyi_result,
                             SH_Idex,week_num,
                             predict_dayloss,shanghai_pop)
    
#    wuhan_pop = 100.71
#    jiaru RainQ fix this value
    wuhan_pop = 90.71
    #    #    some test here blow

#    wuhan_pop = 3792

    predict_dayloss =set()
    predict_dayloss.add(datetime.date(2014,1,1))
    predict_dayloss.add(datetime.date(2014,1,2))
    predict_dayloss.add(datetime.date(2014,1,3))
    WH_DataSet = loadDataSet(wuhanWeather_data_new,
                             WH_weibo_yuyi_result,
                             WH_Idex,
                             week_num,predict_dayloss,wuhan_pop)
#    
#    
#    print BJ_DataSet.shape    
#    saveData_view(WH_DataSet,'BJ_DataSet')
























