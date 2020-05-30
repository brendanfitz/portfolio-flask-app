console.clear()

// set the dimensions and margins of the graph
var margin = {top: 20, right: 40, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// parse the date / time
//var parseTime = d3.timeParse("%d-%b-%y");

// set the ranges
var xBarScale = d3.scaleBand()
    .range([0, width])
    .paddingInner(0.5)
    .paddingOuter(0.25);
var xLineScale = d3.scalePoint()
    .range([0, width])
    .padding(0.5);
var yBarScale = d3.scaleLinear()
    .range([height, 0]);
var yLineScale = d3.scaleLinear()
    .range([height, 0]);

// define the 1st line
var valueline = d3.line()
    .x(function(d) { return xLineScale(d.season_number); })
    .y(function(d) { return yLineScale(d.goals); });

// append the svg obgect to the body of the page
// appends a 'group' element to 'svg'
// moves the 'group' element to the top left margin
var svg = d3.select("#chart-area").append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Get the data
d3.csv("static/js/data/alexander_ovechkin.csv", function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {
      d.season_number = +d.season_number;
      d.goals = +d.goals;
      d.gamesPlayed = +d.gamesPlayed;
  });
	console.table(data);

  update(data);


});

function update(data) {

  // Scale the range of the data
  xBarScale.domain(data.map(function(d) { return d.season_number; }));
  xLineScale.domain(data.map(function(d) { return d.season_number; }));
  yBarScale.domain([0, d3.max(data, function(d) { return d.gamesPlayed; })])
      .nice();
  yLineScale.domain([0, d3.max(data, function(d) { return d.goals; })])
      .nice();

  var rect = g.selectAll("rect")
      .data(data)

  rect.enter().append("rect")
  	.merge(rect)
      .style("stroke", "none")
      .attr("class", "bar barsFill")
      .style("fill", "#82E0AA")
      .attr("x", function(d){ return xBarScale(d.season_number); })
      .attr("width", function(d){ return xBarScale.bandwidth(); })
      .attr("height", function(d){ return height - yBarScale(d.gamesPlayed); })
      .attr("y", function(d){ return yBarScale(d.gamesPlayed); });

  // Add the valueline path.
  g.append("path")
      .data([data])
      .attr("class", "line")
      .style("stroke", "steelblue")
      .attr("d", valueline);

  var points1 = g.selectAll("circle.point1")
      .data(data)

  points1.enter().append("circle")
  	.merge(points1)
      .attr("class", "point1")
      .style("stroke", "steelblue")
  		.style("fill", "steelblue")
      .attr("cx", function(d){ return xLineScale(d.season_number); })
      .attr("cy", function(d){ return yLineScale(d.goals); })
      .attr("r", function(d){ return 5; });


  // Add the X Axis
  g.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(xLineScale));

  // Add the Y0 Axis
  g.append("g")
      .attr("class", "axisSteelBlue")
      .call(d3.axisLeft(yLineScale))
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Goals");

  // Add the Y1 Axis
  g.append("g")
      .attr("class", "barsFill")
      .attr("transform", "translate( " + width + ", 0 )")
      .call(d3.axisRight(yBarScale))
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", -12)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Games Played");
}
