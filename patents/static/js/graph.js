var scriptTag = document.querySelector('script[src$="graph.js"]');
var graphJsonString = scriptTag.dataset.graph;
var data = JSON.parse(graphJsonString);


var links = data.links;
var nodes = data.nodes;

var svg = d3.select("#graph-svg")
    .attr("viewBox", "0 0 800 600")
    .attr("preserveAspectRatio", "xMidYMid meet");

var simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id(function (d) { return d.id; }))
    .force("charge", d3.forceManyBody().strength(-200))
    .force("center", d3.forceCenter(400, 300));

var link = svg.append("g")
    .attr("class", "links")
    .selectAll("line")
    .data(links)
    .enter()
    .append("line")
    .style("stroke", "#999")
    .style("stroke-opacity", 0.6)
    .style("stroke-width", function (d) { return Math.sqrt(d.value); });

var node = svg.append("g")
    .attr("class", "nodes")
    .selectAll("circle")
    .data(nodes)
    .enter()
    .append("circle")
    .attr("r", 10)
    .style("fill", function (d) { return d.type === "plaintiff" ? "lightblue" : "lightgreen"; });

var label = svg.selectAll(".label")
    .data(nodes)
    .enter()
    .append("text")
    .attr("class", "label")
    .attr("text-anchor", "middle")
    .attr("dy", ".35em")
    .text(function(d) { return d.id; });

node.append("title")
    .text(function(d) { return d.id; });

simulation.on("tick", function () {
    link
    .attr("x1", function (d) { return d.source.x; })
    .attr("y1", function (d) { return d.source.y; })
    .attr("x2", function (d) { return d.target.x; })
    .attr("y2", function (d) { return d.target.y; });

    node
    .attr("cx", function (d) { return d.x; })
    .attr("cy", function (d) { return d.y; });

    label
    .attr("x", function (d) { return d.x; })
    .attr("y", function (d) { return d.y; });
});