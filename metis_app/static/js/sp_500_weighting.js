// source: https://bl.ocks.org/alokkshukla/3d6be4be0ef9f6977ec6718b2916d168
var diameter = 600;
var color = d3.scaleOrdinal(d3.schemeCategory10);

dollarfmt = d3.format('$,.2f')
weightfmt = d3.format('.2f')

var tip = d3.tip()
  .attr("class", "d3-tip")
  .html(function(d) {
    console.log(dollarfmt(d.data['Price']));
    console.log(d.data['GICS Sector']);
    var text = "<strong>Company:</strong> <span style='color:#66ccff'>" + d.data['Company']  + "</span><br>";
    text += "<strong>GICS Sector:</strong> <span style='color:#66ccff'>" + d.data['GICS Sector'] + "</span><br>";
    text += "<strong>Price:</strong> <span style='color:#66ccff'>" + dollarfmt(d.data['Price']) + "</span><br>";
    text += "<strong>Weight:</strong> <span style='color:#66ccff'>" + weightfmt(d.data['Weight']) + "</span><br>";
    return text;
  });

d3.json("/api/s%26p500_weighting").then(function(data){
  var dataset = {"children": data}

  var bubble = d3.pack(dataset)
      .size([diameter, diameter])
      .padding(1.5);

  var svg = d3.select("#chart-area")
      .append("svg")
      .attr("width", diameter)
      .attr("height", diameter)
      .attr("class", "bubble");

  var nodes = d3.hierarchy(dataset)
      .sum(function(d) { return d.Weight; });

  console.log(bubble(nodes).descendants())
  var node = svg.selectAll(".node")
      .data(bubble(nodes).descendants())
      .enter()
      .filter(function(d){
          return  !d.children
      })
      .append("g")
      .attr("class", "node")
      .attr("transform", function(d) {
          return "translate(" + d.x + "," + d.y + ")";
      });

  node.append("title")
      .text(function(d) {
          return d.Symbol;
      });

  node.append("circle")
      .attr("r", function(d) {
          return d.r;
      })
      .style("fill", function(d,i) {
          return color(d.data['GICS Sector']);
      })
      .on("mouseover", tip.show)
      .on("mouseout", tip.hide);


  node.append("text")
      .attr("dy", ".2em")
      .style("text-anchor", "middle")
      .text(function(d) {
          return d.data.Symbol;
      })
      .attr("font-family", "sans-serif")
      .attr("font-size", function(d){
          return d.r/5;
      })
      .attr("fill", "white");

  d3.select(self.frameElement)
     .style("height", diameter + "px");

  svg.call(tip);
  }
)
