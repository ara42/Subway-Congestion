import pandas as pd
import numpy as np
import re
import requests
import json
from subway_route import route

sc = pd.read_csv('subwaycode.csv',encoding='cp949')

def cong(st_co,updn, day, time):
    gtr=[0,0,0,0,0,0,0,0,0,0]
    tt=time[0:2]
    url = f"https://apis.openapi.sk.com/puzzle/subway/congestion/stat/car/stations/{st_co}?dow={day}&hh={tt}"
    headers = {
        "accept": "application/json",
        "appkey": ""}  ##########앱 키 설정 필수
    response = requests.get(url, headers=headers)
    if response.status_code ==429:
        print("Too Many Requests")
        return(gtr)
    if response.status_code ==400:
        print("Bad Request")
        return(gtr)
    if response.status_code ==401:
        print("Unauthorized")
        return(gtr)
    if response.status_code ==403:
        print("Forbidden")
        return(gtr)
    if response.status_code ==404:
        print("Not Found")
        return(gtr)
    if response.status_code ==500:
        print("Internal Server Error")
        return(gtr)
    if response.status_code ==504:
        print("Gateway Timeout")
        return(gtr)
    
    jd = json.loads(response.text)
    jd1=jd['contents']
    jd2=jd1['stat']
   
    
        
    kk=[]
    updn=int(updn)
    for i in jd2:
        if i['updnLine']==updn:
            kk.append(i)
    
    n1=[]
    n2=[]
    rr=[]
    for i in kk:
        for j in i['data']:
            for k in j['congestionCar']:
                n1=sum(j['congestionCar'])
                n2.append(n1)
        if sum(n2)!=0:
            rr.append(i)
            n1=[]
            n2=[]
    
    mi=time[2:4]
    mi=str(mi)
    g=[]
    for i in rr:
        for j in i['data']:
            if j['mm']==mi:
                if sum(j['congestionCar'])!=0:
                    g.append(j['congestionCar'])
                    
    for i in range(len(g)):
        while len(g[i])<10:
            g[i].append(0)
    
    g=np.array(g)
    g1=g.mean(axis=0)
    gtt=[]
    for i in g1:
            gtt.append(round(i))
    return(gtt)

def RST(st1, st2, d, h, m):
    B, lt = route(st1, st2, d, h, m)
    
    df=pd.DataFrame(B)
    spst=[]
    for i in range(len(df[2])-1):
        if df[2][i]!=df[2][i+1]:
            spst.append(i+1)
    
    h=re.sub(r'[^0-9]', '', h)
    m=re.sub(r'[^0-9]', '', m)
    
    st_co=[]    #노선도 코드로
    st_na=[]    #노선도 역명으로
    
    for i in B:
        if i[0][-1]!='역':
            nm=i[0]+'역'
        else:
            nm=i[0]
        if nm=='총신대입구역':
            nm='이수역'
        st_na.append(nm)
        li=i[2].split()[0]
        nml=sc[sc.stationName==nm]
        nml2=nml[nml.subwayLine==li]
        try:
            nml3=nml2['stationCode'].values[0]
        except:
            nml3='x'
        st_co.append(nml3)
        
        
    st_time=[]
    for i in B:
        nb = re.sub(r'[^0-9]', '', i[1])
        nbs=round(int(nb[-2:]))
        q1=nb[0:2]
        qq=round(nbs,-1)
        if int(qq)==60:
            q1=int(q1)
            q1=q1+1
            q1=str(q1)
            qq='00'
        if int(q1)==25:
            q1='01'
            
        if len(str(qq))==1:
            ww='0'+str(qq)
        else:
            ww=str(qq)
        ee=q1+ww
        st_time.append(ee)
    
    upd=[]
    for i in range(len(st_co)-1):
        if (st_co[i]>st_co[i+1]):
            upd.append(0) #상행
        else:
            upd.append(1) #하행
    
    upd.append(upd[-1])    
        
    dy=d
    if dy=='월':
        dy='MON'
    elif dy=='화':
        dy='TUE'
    elif dy=='수':
        dy='WED'
    elif dy=='목':
        dy='THU'
    elif dy=='금':
        dy='FRI'
    elif dy=='토':
        dy='SAT'
    elif dy=='일' :
        dy='SUN'

    sst=[]  #칸 혼잡도 숫자
    ssp=[]  #칸 혼잡도 문자
    for i in range(len(st_co)):
        gh=cong(st_co[i],upd[i],dy,st_time[i])
        sst.append(gh)
        ssk=[]
        for i in gh:
            if i==0:
                ssk.append('X')
            elif i<34:
                ssk.append('여유')
            elif i<100:
                ssk.append('보통')
            elif i<170:
                ssk.append('주의')
            else:
                ssk.append('혼잡')
        ssp.append(ssk)
        
    return st_na, sst, ssp, spst, B, df
