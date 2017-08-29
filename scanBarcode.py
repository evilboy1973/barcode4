
import sqlite3
import sys
import urllib
import datetime
from io import open
import csv
import os


def log_values(staff_id):
	conn=sqlite3.connect('/home/pi/Documents/python_project/barcode4/attendance.db')  #It is important to provide an
							     				  #absolute path to the database
							      				  #file, otherwise Cron won't be
							     			 	  #able to find it!
	curs=conn.cursor()
	curs.execute("""INSERT INTO participants values(datetime(CURRENT_TIMESTAMP, 'localtime'),
         (?))""", (temp))
	conn.commit()
	conn.close()


with open('attendance.txt','r',encoding='utf-8') as fin:
	
	count=0
	csvreader=csv.reader(fin,delimiter=',')
	header = next(csvreader)
	list01=list(csvreader)

	#reader the record from the CSV file
	#for row in csvreader:
		#print(','.join(row))
		#count+=1

	print(list01)	
	print(len(list01))
	
	fin.close()

while (sys.stdin.read(1).upper()!='Q'):
		
	line=sys.stdin.readline().rstrip()
		
	if line.upper()=='Q': break	
	
	if line!='':
		d=str(datetime.datetime.now())
		print('The Barcode is :'+line+','+d)
		list01.append([line,d])

	
with open('attendance.txt','w',encoding='utf-8') as fout:
		
	csvwriter=csv.writer(fout,delimiter=',')
	csvwriter.writerow(header)
	
	for rec in list01:
		csvwriter.writerow(rec)
	
	fout.close()

