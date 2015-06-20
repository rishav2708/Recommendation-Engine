import csv
import sys
import requests
import json
headers={"content-type":"application/json"}
csvFile=open("delhi_randomness.csv","rb")
csvFile1=open("hyd_randomness.csv","rb")
csvFile2=open("chennai_randomness.csv","rb")
s=csv.reader(csvFile,delimiter=",")
h=csv.reader(csvFile1,delimiter=",")
c=csv.reader(csvFile2,delimiter=",")
delhi={}
hyd={}
chennai={}
url="http://localhost:7474/db/data/cypher"
for i in s:
	row=i
	delhi[row[0]]=[row[1],row[2],row[3]]
	query={"query":"match (n:Class) where n.class='"+row[0]+"' set n.delhi_randomness="+str(row[3])}
	print requests.post(url,data=json.dumps(query),headers=headers)
	
for i in h:
	row=i
	hyd[row[0]]=[row[1],row[2],row[3]]
	query={"query":"match (n:Class) where n.class='"+row[0]+"' set n.hyd_randomness="+str(row[3])}
	print requests.post(url,data=json.dumps(query),headers=headers)
for i in c:
	row=i
	chennai[row[0]]=[row[1],row[2],row[3]]
	query={"query":"match (n:Class) where n.class='"+row[0]+"' set n.chennai_randomness="+str(row[3])}
	print requests.post(url,data=json.dumps(query),headers=headers)

print delhi,hyd,chennai


