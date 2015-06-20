from alchemyapi import AlchemyAPI
import json
import sys
import requests
import re
headers={"content-type":"application/json"}
al=AlchemyAPI()
indices_dict={}
document={}
elastic="http://localhost:9200/"
masterUrl="http://neo4j:rr@localhost:7474"
def changeType(u):
	u=u.replace("localhost","neo4j:rr@localhost")
	return u
def keywordNodeCreation(keywords):
	nodes=[]
	for i in keywords:
		url=masterUrl+"/db/data/index/node/keywords?uniqueness=get_or_create"
		vector={"key":"keyword","value":i,"properties":{"keyword":i}}
		t=requests.post(url,data=json.dumps(vector),headers=headers).json()
		u=t['self']
		u=u.replace("localhost","neo4j:rr@localhost")
		u+="/labels"
		text="Keyword"	
		print requests.post(u,data=json.dumps(text),headers=headers)
		nodes.append(t['self'])
	return nodes
def createDocNode(document):
	url=masterUrl+"/db/data/node"
	t=requests.post(url,data=json.dumps(document),headers=headers).json()
	u=t['self']
	u=u.replace("localhost","neo4j:rr@localhost")
	u+="/labels"
	text="Document"
	print requests.post(u,data=json.dumps(text),headers=headers)
	return t['self']
def indexCreation(label):
	url=masterUrl+"/db/data/index/node/class?uniqueness=get_or_create"
	vector={"key":"class","value":label,"properties":{"class":label}}
	t=requests.post(url,data=json.dumps(vector),headers=headers).json()
	u=t['self']
	u=u.replace("localhost","neo4j:rr@localhost")
	u+="/labels"
	text="Class"
	print requests.post(u,data=json.dumps(text),headers=headers)
	return t['self']
def entityNodeCreation(entities):
	nodes=[]
	for i in entities.keys():
		url=masterUrl+"/db/data/index/node/"+i+"?uniqueness=get_or_create"
		print url
		for j in entities[i]:
			vector={"key":"name","value":j,"properties":{"name":j}}
			t=requests.post(url,data=json.dumps(vector),headers=headers).json()
			print t
			u=t['self']
			u=u.replace("localhost","neo4j:rr@localhost")
			u+="/labels"
			text=i
			print requests.post(u,data=json.dumps(text),headers=headers)
			nodes.append(t['self'])
	return nodes
def createMultiRels(node1,nodes):
	url="http://neo4j:rr@localhost:7474/db/data/index/relationship/MyIndex/?uniqueness=get_or_create"
	node1=changeType(node1)
	node1+="/relationships"
	for i in nodes:
		u=changeType(i)
		#prop=u+"/properties"
		#d=requests.get(prop).json();
		#k=d.keys()[1]
		rel={"to":u,"type":"CONTAINS"}
		print requests.post(node1,data=json.dumps(rel),headers=headers)
def getDocCount():
	u="http://localhost:9200/_stats"
	t=requests.get(u).json()
	for i in t['indices'].keys():
		indices_dict[i]=t['indices'][i]['total']['docs']['count']
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
url="http://quora-api.herokuapp.com/users/"+sys.argv[1]+"/activity"
data=requests.get(url).json()
data=data['activity']
payload={}
#count=0
#getDocCount()
for activities in data:
	title=activities['title']
	summary=activities['summary']
	print title
	document['title']=title
	document['summary']=summary
	labels=al.taxonomy("text",title)
	entities=al.entities("html",summary)
	keywords=al.keywords("html",summary)
	sentiment=al.sentiment("html",summary)
	#print labels['taxonomy']
	#count+=1
	payload['entities']={}
	payload['keywords']=[]
	payload['sentiment']={}
	docNode=createDocNode(document)
	try:
		print "Yo"
		labels=labels['taxonomy'][0]['label']
		print "Yo1"
		print labels
		labels=func(labels)
		print labels
		entities=entities['entities']
		print "Sub Classification"
		for i in entities:
			try:
				if float(i['relevance'])>=0.2:
					var=i['type']
					if var not in payload['entities'].keys():
						payload['entities'][var]=[]
					try:
						payload['entities'][var].append(i['text'])	
					except:
						print "Can be an organisation"
						d={}
						d['type']= i['disambiguated']['text']
						d['url']= i['disambiguated']['website']
						payload['entities'][var].append(d)
			except:
				print "Not found relevance"
				continue
		print "keywords"
		keywords=keywords["keywords"]
		for j in keywords:
			try:
				if float(j['relevance'])>=0.6:
					payload['keywords'].append(j['text'])
			except:
				continue
		print "sentiment" 
		payload['sentiment']['score']=sentiment['docSentiment']['score']
		payload['sentiment']['type']=sentiment['docSentiment']['type']
		print payload
		for label in labels:
			print "Haaa"
			if label=="":
				print "null label"
				continue
			else:
				print label,payload
				neoIndex=indexCreation(label)
				neoIndex=neoIndex.replace("localhost","neo4j:rr@localhost")
				payload['idx_location']=neoIndex
				neoIndex+="/relationships"
				print neoIndex
				rel={"to":changeType(docNode),"type":"IS_INDEXED"}
				requests.post(neoIndex,data=json.dumps(rel),headers=headers)
				objects=entityNodeCreation(payload['entities'])
				payload['entity_location']=objects
				keys=keywordNodeCreation(payload['keywords'])
				payload['keys_location']=keys
				createMultiRels(docNode,objects)
				createMultiRels(docNode,keys)
				url1=elastic+label+"/data/"
				print url1
				payload['keywords'].append(label)
				print url1,payload
				print requests.post(url1,data=json.dumps(payload))
	except:
		#print "There is an error"
		continue