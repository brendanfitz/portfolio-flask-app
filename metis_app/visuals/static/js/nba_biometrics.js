var margin = {top: 15, right: 10, bottom: 22.5, left: 30},
    width = 720 - margin.left - margin.right,
    height = 375 - margin.top - margin.bottom;

var colorColumn, dataCleaned, opacity;

colorColumn = 'DBSCAN Results';
opacity = 0.65
/* 
 * value accessor - returns the value to encode for a given data object.
 * scale - maps value to a visual display encoding, such as a pixel position.
 * map function - maps from data value to display value
 * axis - sets up axis
 */ 

// setup x 
var xValue = function(d) { return d['Height (Inches)']; }, // data -> value
    xScale = d3.scaleLinear().range([0, width]), // value -> display
    xMap = function(d) { return xScale(xValue(d)); }, // data -> display
    xAxis = d3.axisBottom(xScale);

// setup y
var yValue = function(d) { return d["Weight"]; }, // data -> value
    yScale = d3.scaleLinear().range([height, 0]), // value -> display
    yMap = function(d) { return yScale(yValue(d)); }, // data -> display
    yAxis = d3.axisLeft(yScale);

var colorMap = {
    'DBSCAN Results': {
      'Core Data': '#2874A6',
      'Outlier': '#00ffc5',
    },
    'IsolationForest Results': {
      'Core Data': '#2874A6',
      'Outlier': '#de03f9',
    },
    'PCA Z-Score Results': {
      'Core Data': '#2874A6',
      'Outlier': '#fbfd00',
    },
}
function color(d) {
  var cmap = colorMap[colorColumn];
  outlier_status = d[colorColumn];
  return cmap[outlier_status];
}

// add the graph canvas to the body of the webpage
var svg = d3.select("#chart-area")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);
  g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// add the tooltip area to the webpage
var tooltip = d3.select("body").append("div")
    .attr("class", "tooltip")
    .style("opacity", 0);

// load data
d3.csv("/visuals/static/js/data/nba_biometrics_analysis.csv").then(function(data) {

  // change string (from CSV) into number format
  data.forEach(function(d) {
    d["Height (Inches)"] = +d["Height (Inches)"];
    d["Weight"] = +d["Weight"];
//    console.log(d);
  });

  // don't want dots overlapping axis, so add in buffer to data domain
  var xbuffer = 1;
  var ybuffer = 10;
  xScale.domain([d3.min(data, xValue)-xbuffer, d3.max(data, xValue)+xbuffer]);
  yScale.domain([d3.min(data, yValue)-ybuffer, d3.max(data, yValue)+ybuffer]);

  // x-axis
  g.append("g")
      .attr("class", "x axisNBA")
      .style("font-size", "0.75rem")
      .attr("transform", "translate(0," + height + ")")
      .call(xAxis)
    .append("text")
      .attr("class", "label")
      .attr("x", width)
      .attr("y", -6)
      .style("text-anchor", "end")
      .text("Height (Inches)");

  // y-axis
  g.append("g")
      .style("font-size", "0.75rem")
      .attr("class", "y axisNBA")
      .call(yAxis)
    .append("text")
      .attr("class", "label")
      .attr("transform", "rotate(-90)")
      .attr("y", 6)
      .attr("dy", ".71em")
      .style("text-anchor", "end")
      .text("Weight (lbs)");

  // draw dots
  g.selectAll(".dot")
      .data(data)
    .enter().append("circle")
      .attr("class", "dot")
      .attr("r", 3.5)
      .attr("cx", xMap)
      .attr("cy", yMap)
      .style("fill", function(d) { return color(d);}) 
      .style("opacity", opacity)
      .on("mouseover", function(d) {
          tooltip.transition()
               .duration(200)
               .style("opacity", .9);
          tooltip.html("<strong>" + d["Player"] + "</strong><br/> (" + xValue(d) 
	        + " in, " + yValue(d) + " lbs)")
               .style("font-size", "0.75rem")
               .style("left", (d3.event.pageX + 10) + "px")
               .style("top", (d3.event.pageY - 15) + "px");
      })
      .on("mouseout", function(d) {
          tooltip.transition()
               .duration(500)
               .style("opacity", 0);
      });

  // draw legend
  var legend = g.selectAll(".legend")
      .data(Object.keys(colorMap[colorColumn]))
    .enter().append("g")
      .attr("class", "legend")
      .attr("transform", function(d, i) { return "translate(0," + i * 20 + ")"; });

  // draw legend colored rectangles
  legend.append("rect")
      .attr("x", width - 18)
      .attr("y", height - 100 - 9)
      .attr("width", 18)
      .attr("height", 18)
      .style("fill", function(d) { return colorMap[colorColumn][d]; })
      .style("opacity", opacity)
      .style("stroke", "rgb(0,0,0)")
      .style("stroke-width", "1px");

  // draw legend text
  legend.append("text")
      .attr("x", width - 24)
      .attr("y", height - 100)
      .attr("dy", ".35em")
      .style("text-anchor", "end")
      .style("font-size", "0.75rem")
      .text(function(d) { return d;})
  
  dataCleaned = data;
});

$('#modelSelect').on('change', function() {
  colorColumn = this.value + ' Results';
  console.log(colorColumn);
  changeColor(dataCleaned);
})

function changeColor(data) {
  var rects = d3.selectAll(".dot")
    .data(data)
  rects.style("fill", function(d) { return color(d); }) 

  var legend_boxes = d3.selectAll('.legend')
    .select('rect')
  legend_boxes.style("fill", function(d) { return colorMap[colorColumn][d]; });
}