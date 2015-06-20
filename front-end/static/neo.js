    function idIndex(a,id) {
      for (var i=0;i<a.length;i++) 
        {if (a[i].id == id) return i;}
      return null;
    }  
    function isInGroups(value,array){
      if(array.indexOf(value) < 0)
      {
        array.push(value)
        return 2*array.indexOf(value);
      }
      else 
      {
        return 2*array.indexOf(value);
      }
    }
   /* function relatedClass(c)
    {
      var uname = "neo4j";
       var pswd = "rr";
       Authorizationkey = uname+':'+pswd;
       Authorizationkey = btoa(Authorizationkey);
       key = "Basic "+Authorizationkey;
       link ="http://neo4j:rr@192.168.1.30:7474/db/data/cypher";
       var k="match (n)-[r:INHERITS]-(v) where n.class='"+c+"' return distinct v.class;",
       $.ajax({
        url:link,
        type:"POST",
        data:{query:k},
        success:function(resp,data,xhr)
        {
          alert(resp)
        }
       });
    }*/

    function clicking(){
      var k1 = document.getElementById("sample").value;
      //relatedClass(k1)
      var k="match (n:Class)-[r:INHERITS]-(n1) where n.class='"+k1+"'with  collect(n1.class) as ext start p=node:places('withinDistance:[28.6138967, 77.2159562,10.0]') match (p)-[r]-(c:Class) where c.class in ext return p.name,p.type limit 20;"
       var uname = "neo4j";
       var pswd = "rr";
       Authorizationkey = uname+':'+pswd;
       Authorizationkey = btoa(Authorizationkey);
       key = "Basic "+Authorizationkey;
       console .log(Authorizationkey);
      var post_data ={
       "statements":[{
         "statement": k,
         "resultDataContents":["graph"]
       }]
     };
     link ="http://192.168.1.30:7474/db/data/transaction/commit";

     $.ajax({
       headers:{"Authorization": key},
       type: "POST",
       accept: "application/json",
       contentType:"application/json; charset=utf-8",
       url: link,
       data: JSON.stringify(post_data),
       success: function(data, textStatus, jqXHR){
         draw_forced_directory(data);
       },
       failure: function(msg){
         alert("failed");
       }
     });
   }


   function draw_forced_directory(data){
          //Creating graph object
          try{
            d3.select("#neooutput")
            .selectAll("svg")
            .remove();
            d3.select("#neooutput")
            .selectAll("p")
            .remove();
            var color = d3.scale.category10();
            var nodes=[], links=[];
            var groups=[];
            console.log(data);
            data.results[0].data.forEach(function (row) {
              console.log(row);
              row.graph.nodes.forEach(function (n) 
              {
                if (idIndex(nodes,n.id) == null)
                  nodes.push({id:n.id,label:n.labels[0],title:n.properties,group:isInGroups(n.labels[0],groups)});
              });
              links = links.concat( row.graph.relationships.map(function(r) {
                return {source:idIndex(nodes,r.startNode),target:idIndex(nodes,r.endNode),type:r.type, value:1};
              }));
            });
            console.log(JSON.stringify(links));
            graph = {nodes:nodes, links:links};
            k=JSON.stringify(graph);
    // force layout setup
    var width = 1000, height = 800;
    var force = d3.layout.force()
    .charge(-200).linkDistance(55).size([width, height]);

    // setup svg div
    var svg = d3.select("#neooutput").append("svg")
    .attr("width", "1500").attr("height", "800")
    .attr("pointer-events", "all");

    // load graph (nodes,links) json from /graph endpoint
    force.nodes(graph.nodes).links(graph.links).start();

    // render relationships as lines
    var link = svg.selectAll(".link")
    .data(graph.links).enter()
    .append("line").attr("class", "link")
    .style("stroke-width",2);

    // render nodes as circles, css-class from label
    var node = svg.selectAll(".node")
    .data(graph.nodes).enter()
    .append("g")
    .attr("class", function (d) { return "node "+d.label; })
    .on("mouseover",mouseover)
    .on("mouseout",mouseout)
    .append("circle")
    .attr("r",8)
    .style("fill","white")
    .style("stroke", function(d) { return color(d.group);})
    .style("stroke-width",3)
    .call(force.drag);

    svg.selectAll("text")
        .data(graph.links)
        .enter()
        .append("text")
        .text(function(d){ return "relationship: "+d.type})
        .attr("x", function (d){ (d.source.x+d.target.x)/2})
        .attr("y", function (d){ (d.source.y+d.target.y)/2});

    function mouseover() {
      d3.select(this).select("circle").transition()
      .duration(750)
      .attr("r", 12)
      .style("fill",function(d) { return color(d.group);});
    }

    function mouseout() {
      d3.select(this).select("circle").transition()
      .duration(750)
      .attr("r", 8)
      .style("fill","white");
    }


    // html title attribute for title node-attribute
    node.append("title")
    .text(function (d) { 
     content = "";

     for (x in d.title)
     {
      content += x+":  "+String(d.title[x])+"\n"
    } ;
    return content;
  });

    // force feed algo ticks for coordinate computation
    force.on("tick", function() {
      link.attr("x1", function(d) { return d.source.x; })
      .attr("stroke", "#999")
      .attr("y1", function(d) { return d.source.y; })
      .attr("x2", function(d) { return d.target.x; })
      .attr("y2", function(d) { return d.target.y; });

      node.attr("cx", function(d) { return d.x; })
      .attr("cy", function(d) { return d.y; });
    });}
    catch(err){d3.select("#neooutput")
    .append("p")
    .text("error")
    .style("color","red");}
  };
