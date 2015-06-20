import requests
import json
import sys
import simplejson as js
from alchemyapi import AlchemyAPI
#al=AlchemyAPI()
neoUrl="http://neo4j:rr@localhost:7474/db/data/cypher"
headers={"content-type":"application/json"}
def func(labels):
	k=[]
	labels=labels.replace("and","/")
	li=labels.split("/")
	for labels in li:
		#print l
		l=re.findall('([a-zA-Z0-9]+)\sand\s([a-zA-Z0-9]+)',labels)
		if len(l)==0:
			l=re.findall('[a-zA-Z0-9]+',labels)
			l='-'.join(l)
			k.append(l)
			
		else:
			for i in range(len(l)):
				l[i]='-'.join(l[i])
			k.append(l[0])
	return k
data=js.loads(open("records.json").read())
headers={"content-type":"application/json"}
payload={"query":{"query_string":{"query":"*"+sys.argv[1]+"*"}}}
elastic_url="http://localhost:9200/entities/_search"
resp=requests.post(elastic_url,data=json.dumps(payload)).json()
typo=""
if len(resp['hits']['hits'])>0:
	typo=resp['hits']['hits'][0]['_type']
	#print func(al.taxonomy("text",typo)['taxonomy'][0]['label'])

try:
	if typo=="":
		print data[sys.argv[1]]

	else:
		print typo
except:
	print "Under Construction"
