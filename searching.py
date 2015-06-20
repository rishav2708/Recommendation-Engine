import requests
import sys
import json
from urllib import urlencode
query=sys.argv[1]
headers={"content-type":"application/json"}
url="http://localhost:9200/_search" 
query=query.replace(" ","+")
d={"q":query}
d=urlencode(d)
url+=("?"+d)
#url+=query
print url
resp=requests.get(url).json()
try:
	respnose=resp['hits']['hits'][0]['_index']
	url="http://neo4j:rr@localhost:7474/db/data/cypher"
	query="""start n=node:class(class='"""+respnose+"""')
	match n-[r:IS_INDEXED]->(b:Document)<-[r1:IS_INDEXED]-c return  n.class,c.class;""" 
	d={"query":query}
	t=requests.post(url,data=json.dumps(d),headers=headers).json()
	print t
except:
	print "Not found"