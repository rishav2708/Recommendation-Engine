import requests
import json
import nltk
url="http://neo4j:rr@localhost:7474/db/data/cypher"
url1="http://localhost:9200/mydocs/first/"
query={"query":"match (n:Document) return id(n),n.title,n.summary"}
headers={"content-type":"application/json"}
resp=requests.post(url,data=json.dumps(query),headers=headers).json()
resp=resp['data']
uri="http://neo4j:rr@localhost:7474/db/data/node/"
payload={}
for i in resp:
	elastic=url1+str(i[0])
	payload['link']=uri+str(i[0])
	payload['title']=i[1]
	payload['content']=nltk.clean_html(i[2])
	#print url1
	print elastic
	print payload
	print requests.put(elastic,data=json.dumps(payload)).json()
