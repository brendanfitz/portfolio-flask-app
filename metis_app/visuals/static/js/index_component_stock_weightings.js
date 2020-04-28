// source: https://bl.ocks.org/alokkshukla/3d6be4be0ef9f6977ec6718b2916d168
var diameter = 600;
var margin = { left:0, right:0, top:0, bottom:300 };
var color = d3.scaleOrdinal(d3.schemeCategory10);

dollarfmt = d3.format('$,.2f')
weightfmt = d3.format('.2f')

var tip = d3.tip()
  .attr("class", "d3-tip")
  .html(function(d) {
    console.log(dollarfmt(d.data['Price']));
    console.log(d.data['Industry']);
    var text = "<strong>Company:</strong> <span style='color:#66ccff'>" + d.data['Company']  + "</span><br>";
    text += "<strong>Industry:</strong> <span style='color:#66ccff'>" + d.data['Industry'] + "</span><br>";
    text += "<strong>Price:</strong> <span style='color:#66ccff'>" + dollarfmt(d.data['Price']) + "</span><br>";
    text += "<strong>Weight:</strong> <span style='color:#66ccff'>" + weightfmt(d.data['Weight']) + "</span><br>";
    return text;
  });

index = $("p#StockIndex").text()
uri = "/api/index_component_stocks/" + index

d3.json(uri).then(function(data){
  var dataset = {"children": data}

  var bubble = d3.pack(dataset)
      .size([diameter, diameter])
      .padding(1.5);

  var svg = d3.select("#chart-area")
      .append("svg")
      .attr("width", diameter + margin.left + margin.right)
      .attr("height", diameter + margin.top + margin.bottom)
      .attr("class", "bubble");

  var g = svg.append("g")
          .attr("transform", "translate(" + margin.left +
              ", " + margin.top + ")");

  var nodes = d3.hierarchy(dataset)
      .sum(function(d) { return d.Weight; });

  var node = g.selectAll(".node")
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
          return color(d.data['Industry']);
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

  industries = [];
  data.forEach(function(d) {
      if (!industries.includes(d['Industry'])) {
        industries.push(d['Industry']);
    }
  });
  industries.sort();

  var legend = svg.append('g')
    .attr("transform", "translate(" + (diameter / 2) + ", " + (diameter + 20) + ")")

  industries.forEach(function(industry, i) {
    var legendRow = legend.append("g")
      .attr("transform", "translate(0, " + (i * 20) + ")");

    legendRow.append("rect")
      .attr("width", 10)
      .attr("height", 10)
      .attr("fill", color(industry));

    legendRow.append("text")
      .attr("x", -10)
      .attr("y", 10)
      .attr("text-anchor", "end")
      .style("text-transform", "capitalize")
      .text(industry);

  })

})
