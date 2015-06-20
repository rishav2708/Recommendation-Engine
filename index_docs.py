import requests
import json
headers={"content-type":"application/json"}
url="http://neo4j:rr@localhost:7474/db/data/cypher"
url1="http://neo4j:rr@localhost:7474/db/data/index/node/myDocs?uniqueness=get_or_create"
query={"query":"match (n:Document) return id(n),n.title"}
resp=requests.post(url,data=json.dumps(query),headers=headers).json()
resp=resp['data']
uriNode="http://neo4j:rr@localhost:7474/db/data/node/"
for i in resp:
	uri=uriNode+str(i[0])
	vector={"key":"doc","value":i[0],"uri":uri}
	print requests.post(url1,data=json.dumps(vector),headers=headers)
