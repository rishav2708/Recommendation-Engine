import requests
import json
import sys, numpy, scipy
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
headers={"content-type":"application/json"}
url="http://neo4j:rr@localhost:7474/db/data/cypher"
query={"query":"match (n:Class) return distinct n.class"}
classes=requests.post(url,data=json.dumps(query),headers=headers).json()['data']
d={}
for i in classes:
	d[i[0]]={}
	for j in classes:
		d[i[0]][j[0]]=0
query={"query":"match (n:Class)-[r:IS_INDEXED]->(b:Document)<-[r1:IS_INDEXED]-(c:Class) return n.class,c.class,count(b)"}
res=requests.post(url,data=json.dumps(query),headers=headers).json()
res=res['data']
#print res
for i in res:
	d[i[0]][i[1]]=i[2]
n=len(d.keys())
l=d.keys()
#print l
f=numpy.zeros((n,n))
#print f
#for key1 in d:
#	print key1
#	print "  "+str(len(d[key1].keys()))

for i in range(n):
	for j in range(n):
#		print i,j
		f[i,j]=d[l[i]][l[j]]
dist_mat=dist.pdist(f)
linkage=hier.linkage(dist_mat)
dendo=hier.dendrogram(linkage)
#print linkage
#print len(linkage)
#print dendo'
leaves=dendo['leaves']
#print dendo['leaves']