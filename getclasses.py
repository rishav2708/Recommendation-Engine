from view import *
import sys
import json
import requests
n=len(l)
global nums
dicti={}
def precompute():
	for i in l:
		dicti[i]=my_func(i)
	fp=open("records.json","w")
	json.dump(dicti,fp)
def my_func(stri):
	try:
		li= my_traverse(stri)
		nums=[]
		query={"query":"match (n:Class)-[r]-(d:Document)-[r1]-(c:Class) where n.class='"+stri+"' return c.class"}
		response=requests.post(url,data=json.dumps(query),headers=headers).json()
		response=response['data']
		li1=[]
		for i in response:
			li1.append(i[0])
	#print li
		if len(li1)<len(li):
			print list(set(li1))
			return list(set(li1))
		elif len(li)<len(li1) :
		#print li
			print list(set(li))
			return list(set(li))
	except:
		print "No key found"
precompute()
