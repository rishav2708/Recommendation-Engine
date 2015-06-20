from cluster import dendo
from cluster import l,linkage
from matplotlib.pyplot import *
import requests
import scipy
classlen=len(l)
#match (n:Class)-[r]-(b:Document)-[r1]-(c:Class) where n.class='music' return n,c;
headers={"content-type":"application/json"}
url="http://neo4j:rr@localhost:7474/db/data/cypher"
dnum={}
d={}
mapper={}
mytree={}
nums=[]
def plot_tree( P, pos=None ):
    icoord = scipy.array( P['icoord'] )
    dcoord = scipy.array( P['dcoord'] )
    color_list = scipy.array( P['color_list'] )
    xmin, xmax = icoord.min(), icoord.max()
    ymin, ymax = dcoord.min(), dcoord.max()
    if pos:
        icoord = icoord[pos]
        dcoord = dcoord[pos]
        color_list = color_list[pos]
    for xs, ys, color in zip(icoord, dcoord, color_list):
        plot(xs, ys,  color)
    xlim( xmin-10, xmax + 0.1*abs(xmax) )
    ylim( ymin, ymax + 0.1*abs(ymax) )
    show()
def rec_fun(num,n):
	if num<n:
		return
	else:
		idx=num-n
		#print idx
		arr=[linkage[idx][0],linkage[idx][1],linkage[idx][2],linkage[idx][3]]
		dnum[num].append(arr)
		d[linkage[idx][0]]=num
		d[linkage[idx][1]]=num
		rec_fun(linkage[idx][0],n)
		rec_fun(linkage[idx][1],n)
def traverse(num,n):
	if num<n:
		#print l[int(num)]
		nums.append(l[int(num)])
		#print li
	else:
		#print dnum[num][0][2],num
		traverse(dnum[num][0][0],n)
		traverse(dnum[num][0][1],n)
def my_traverse(stri):
	idx=d[mapper[stri]]
	global nums
	traverse(idx,classlen)
	return nums
for i in range(len(dendo['ivl'])):
	dendo['ivl'][i]=l[int(dendo['ivl'][i])]
maxi=-1
for i in range(classlen-1):
	if maxi<linkage[i][0]:
		maxi=linkage[i][0]
	if maxi<linkage[i][1]:
		maxi=linkage[i][1]
#dnum={}
for i in range(classlen,int(maxi)+1):
	dnum[i]=[]
	d[i]=0
dendo
rec_fun(maxi,classlen)
#show()
#print dnum    
#print d
for i in range(len(l)):
	mapper[l[i]]=i
#rec_show(266,145)
traverse(147,classlen)
plot_tree(dendo)
