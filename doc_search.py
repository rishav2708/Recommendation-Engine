import requests
import json
url="http://localhost:9200/_search?pretty=true"
c="programming"
query={"query":
				{"query_string":
					{   "query":
							      c}}}


t=requests.post(url,data=json.dumps(query)).json()
print t['hits'['hits']														