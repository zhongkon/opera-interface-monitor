#!/usr/bin/python3
# coding=utf-8
## Script By Zhong
import datetime
import os.path
from os import path
import time
import requests

logFIASOpera = 'c:/Fidelio/IFC8/M87/OPERA_PMS1_'+ str(datetime.datetime.now().day) +'.RTF' # log ของ interface ฝั่ง opera ตอนนี้ไม่ได้ใช้ ใส่ใว้ก่อนเผื่อใช้งาน
logFIAS = 'c:/Fidelio/IFC8/M87/M87POS_IFC1_'+ str(datetime.datetime.now().day) +'.RTF' # log path แก้ให้ตรงกับ interface ที่ต้องการตรวจสอบเน้อ
latestlog = "C:/Fidelio/MonitorTools/latestlog" # ไฟล์เอาใว้เก็บ เวลาล่าสุดที่แจ้งเตือนจะได้ไม่ต้องแจ้งตือนซ้ำ ใน log file อาจมีหลาย ซัำกันหลายที่ 
token = 'กกกกกกกกกกกกกกกกกกกกกกกกกกก' # line notify token gen token เอามาใส่นะครับ 
message = "Micros Interface Link Down " # ข้อความแจ้งเตือน แก้ตามความเหมาะสม
today = datetime.datetime.now()
logstoday = "[" + today.strftime("%m") + "." + today.strftime("%d") +"/" 

def GetLastTime(file_url):
    if path.exists(file_url):
        return float(open(file_url).readline().rstrip())
    else:
        with open(file_url, "w") as f:
            f.write(str(time.time()))
        return  datetime.datetime.timestamp(datetime.datetime.now())

def send_line(msg,token):
    url = 'https://notify-api.line.me/api/notify'
    headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+ token}
    r = requests.post(url, headers=headers , data = {'message':msg})
    print (r.text)

if __name__ == '__main__':

    with open(logFIAS, 'r') as file:
        for line in file:
            if logstoday in line:
                if ("<MessLvl3> ChangeLinkState:End" in line) or ("<MessLvl3> CommTcpServClass --> ConnectEvent" in line) :
                    date_time = datetime.datetime.strptime(today.strftime("%x") + " " + line[12:20], '%m/%d/%y %H:%M:%S')                
                    if datetime.datetime.timestamp(date_time) > GetLastTime(latestlog) :
                        #print(line)
                        send_line(message + line[4:54],token)
                        with open(latestlog, "w") as f:
                            f.write(str(datetime.datetime.timestamp(date_time)))
