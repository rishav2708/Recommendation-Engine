from get_all_entities import *
import sys
print url1
print headers
result=[]
typo=""
u="http://localhost:9200/entities/"
for i in entities:
	url=u+i
	query={"query":"match (n:"+i+") return n.name,id(n)"}
	resp=requests.post(url1,data=json.dumps(query),headers=headers).json()
	d={}
	d['data']=[]
	for i in resp['data']:
		#print i[1]
		d['data'].append(i[0])
		d['url']="http://neo4j:rr@localhost:7474/db/data/node/"+str(i[1])
	print requests.post(url,data=json.dumps(d))

	#query={"query":"match (n:"+i+")-[r]-(b:Document)-[r1]-(c:Class) where n.name=~'.*(?i)"+sys.argv[1]+".*' return distinct n.name,c.class "}
	#print query
	#print i
#print (result),typo