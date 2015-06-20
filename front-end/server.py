from flask import Flask,render_template,request
import requests
import json
import simplejson as js
import threading
from werkzeug.contrib.cache import SimpleCache
url="http://localhost:9200/_search"
nonsecureUrl="http://localhost:7474/db/data/cypher"
headers={"content-type":"application/json"}
cache=SimpleCache()
data=open("records.json").read()
data=js.loads(data)
app=Flask(__name__)
buff=[]
byType={}
byName={}
class FuncThread(threading.Thread):
	def __init__(self,target,*args):
		self._target=target
		self._args=args
		threading.Thread.__init__(self)
	def run(self):
		self._target(*self._args)
def synchronized(function):
	function.__lock__=threading.Lock()
	  #before entering the critical section
	def synced_func(*args,**kews):
		#this is a critical section
		with function.__lock__:
			return function(*args,**kews)
	return synced_func
@synchronized
def search_by_type(args):
	query={"query":args}
	resp=requests.post(nonsecureUrl,data=json.dumps(query),headers=headers).json()['data']
	for i in resp:
		byType[i[3]]=zip(i[0],i[1],i[2])
	print byType
@synchronized
def search_with_sync(args):
	query={"query":args}
	t=requests.post(nonsecureUrl,data=json.dumps(query),headers=headers).json()['data']
	byName['related_class']=[]
	byName['places']=[]
	for i in t:
		myPlaces=i[1]
		myType=i[2]
		byName['related_class']=[k for k in i[0] if k not in byName['related_class']]
		byName['places'].append(tuple((myPlaces,myType)))
@app.route('/results')
def results():
	resp=request.args["q"]
	print resp
	p={"query":{"query_string":{"query":resp}}}
	print p
	res=requests.post(url,data=json.dumps(p)).json()
	res=res['hits']['hits']
	l=[]
	for i in res:
		print i['_index']
		print i['_score']
		l1=[i['_index'],i['_score']]
		print l1
		l.append(l1)
	print l
	return json.dumps(l)
@app.route('/')
def hello():
	return render_template("index.html")
@app.route('/suggest')
def fun1():
	global buff
	global byType
	global byName
	byType={}
	byName={}
	resp=request.args["q"]
	print resp
	query1="""start p=node:place('withinDistance:[28.6139,77.2090,30.0]') match p where p.name=~'.*(?i)"""+resp+""".*'
with collect (distinct p.name) as places,p.type as type
match (c:Class)-[r]-(c1:Class) where c.class=type
return collect( distinct c1.class) as classes,places,type"""
	query2="""match (n:Class)-[r:INHERITS]->(n1) where n.class=~'.*(?i)"""+resp+"""*.' 
with  collect( distinct n1.class) as ext,n
start p=node:place('withinDistance:[28.6138967, 77.2159562,30.0]') match (p)-[r1]-(c:Class) where c.class in ext or c.class=n.class with 
case c.class
when n.class
then collect (distinct p) 
else
collect (distinct p)  end  as result,p.type as types,c
return extract(n IN result| n.name) as names,extract(b in result|b.rating) as ratings,extract(c in result|c.phone) as contacts,types,c.delhi_randomness as randomness order by randomness;"""
	print query1,query2
	thread1=FuncThread(search_with_sync,query1)
	thread2=FuncThread(search_by_type,query2)
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()
	d={}
	d['res1']=byName
	d['res2']=byType
	print byName
	return json.dumps(d)
if __name__ == '__main__':
	app.run()
