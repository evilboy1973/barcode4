from gtts import gTTS
import arrow
import sqlite3
import sys
import urllib
import datetime
from io import open
import csv
import os
import plotly.plotly as py
from plotly.graph_objs import *
import plotly.graph_objs as go


def speakText(text01):
    tts=gTTS(text=text01,lang='en')
    tts.save("temp01.mp3")
    os.system("mpg123 temp01.mp3")

def log_values(staff_id):
    conn=sqlite3.connect('/home/pi/Documents/python_project/barcode4/attendance.db')  #It is important to provide an
    curs=conn.cursor()
    curs.execute("INSERT INTO participants values(datetime(CURRENT_TIMESTAMP, 'localtime'),(?))", [staff_id])
    conn.commit()
    conn.close()


def load_values():
    conn=sqlite3.connect('/home/pi/Documents/python_project/barcode4/attendance.db')
    curs=conn.cursor()
    curs.execute("SELECT * FROM participants")
    participants = curs.fetchall()
    conn.close()
    return participants


def load_values_group():
    conn=sqlite3.connect('/home/pi/Documents/python_project/barcode4/attendance.db')
    curs=conn.cursor()
    curs.execute("select strftime('%Y',rDateTime) as valYear,strftime('%m',rDateTime) as valMonth,strftime('%d',rDateTime) as valDay,strftime('%H',rDateTime) as valHour,count(staffID) from participants group by valDay,valHour")
    participants = curs.fetchall()
    conn.close()
    return participants


def to_plotly_group(rRecord):

    time_series_adjusted_DateTime  = []
    time_series_StaffIDCount = []
        
    for record in rRecord:
        time_series_adjusted_DateTime.append(str(record[0])+str(record[1])+str(record[2])+str(record[3]))
        time_series_StaffIDCount.append(record[4])
        data=[go.Bar(
        x=time_series_adjusted_DateTime,
        y=time_series_StaffIDCount
        )]
    
    plot_url = py.iplot(data, filename='lab_count_participants')
    return plot_url


def to_plotly(rRecord):
    
    timezone='US/Pacific'
    time_series_adjusted_DateTime  = []
    time_series_StaffID = []

    for record in rRecord:
        local_timedate = arrow.get(record[0], "YYYY-MM-DD HH:mm").to(timezone)
        time_series_adjusted_DateTime.append(local_timedate.format('YYYY-MM-DD HH:mm'))
        time_series_StaffID.append(record[1])


    temp = Scatter(
        x=time_series_adjusted_DateTime,
        y=time_series_StaffID,
        name='Number of Participants'
        )
    
    data = Data([temp])
    layout = Layout(
        title="Number of Participants to the Session",
    xaxis=XAxis(
            type='date',
            autorange=True
        ),
                    
        yaxis=YAxis(
            title='Number',
            type='linear',
            autorange=True
        )
    )
    fig = Figure(data=data, layout=layout)
    plot_url = py.plot(fig, filename='lab_count_participants')
    return plot_url

def validate_date(d):
    try:
        datetime.datetime.strptime(d, '%Y-%m-%d %H:%M')
        return True
    except ValueError:
        return False

def readGroup():
    listTemp=[]
    for row in load_values_group():
        listTemp.append([row[0],row[1],row[2],row[3],row[4]]);
    return listTemp

def checkRecord(staffID):
    conn=sqlite3.connect('/home/pi/Documents/python_project/barcode4/attendance.db')
    curs=conn.cursor()
    curs.execute('select * from namelist where sid=(?)',(staffID,))
    matchList = curs.fetchone()
    conn.close()
    return matchList

def main():
    list01=[]
    list02=[]
    
    for row in load_values():   
        print(row[0],row[1])
        list01.append([row[0],row[1]])

    while (sys.stdin.read(1).upper()!='Q'):
        line=sys.stdin.readline().rstrip()
        if line.upper()=='Q': break 
        if line!='':
            d=str(datetime.datetime.now())
            print('The Barcode is :'+line+','+d)
            tempName=checkRecord(str(line))
            if tempName!=None:
                print("Hello!"+tempName[2]+" "+tempName[1])
                speakText("Hello "+tempName[2]+" "+tempName[1])
                speakText("Welcome to Digital Learning exhibition.")
            list01.append([d,line])
            log_values(line)                
            list02=readGroup()
            to_plotly_group(list02)
    return 0

if __name__ =='__main__':
    main()
