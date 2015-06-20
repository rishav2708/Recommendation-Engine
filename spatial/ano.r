library(RNeo4j)
library(ape)
compute=function(csvFile)
{
  #csvFile=read.csv(csvName)
  #print (str(csvFile))
  d=as.matrix(dist(cbind(csvFile$lat,csvFile$lon)))
  d=(1/d)
  for(i in 1:length(d))
  {
    if(d[i]==Inf)
    {
      d[i]=0
    }
  }
  csvFile$typo=as.numeric(as.factor(csvFile$typo))
  return(Moran.I(csvFile$typo,d))  #if any value returns error then we do not have dispersed data and solution is simply custered
  
  
  
}
graph=startGraph("http://localhost:7474/db/data")
query="match (n:Class) return distinct n.class as  classes"
classes=cypher(graph,query)
#print (graph)
#print (st)
x=data.frame()
#x=rbind(x,c("class","observed","expected","p-value"))
for (i in 1:length(classes$classes))
{
  myquery=paste("match (n:Class)-[r]-(c1:Class) where n.class=~'.*",classes$classes[i],"*.' with collect(distinct c1.class) as ext,n start p=node:place('withinDistance:[13.0827,80.2707,15.0]') match (p) where p.type in ext or p.type=n.class return p.lat as lat,p.lon as lon,p.type as typo",sep='')
  st=cypher(graph,myquery)
  #print (str(st))
  tryCatch(

            {
             print (classes$classes[i])
              print (compute(st))
              result=data.frame(compute(st))
              x=rbind(x,c(classes$classes[i],result$observed,result$expected,result$p.value))
              #print (result$observed)
              #x$class=class
              #write.table()
              #plot(compute(st))
            },
            error=function(cond)
            { }
    )
}
#print (x)
#mquery="match (n:Class)-[r]-(c1:Class) where n.class=~'.*school*.' with collect(distinct c1.class) as ext,n start p=node:place('withinDistance:[28.61,77.21,15.0]') match (p) where p.type in ext or p.type=n.class return p.lat as lat,p.lon as lon,p.type as typo"
#st=cypher(graph,mquery)
#print (st)
#print (compute(st))

#x=colnames("class","observed","expected")
colnames(x)=c("class","observed","expected","p-value")
write.table(x,file="chennai_randomness.csv",sep=",",row.names=FALSE,col.names = TRUE)