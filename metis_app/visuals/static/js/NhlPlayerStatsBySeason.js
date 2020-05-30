console.clear()

var formattedData;
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

var xAxisGroup = g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height +")");

var yAxisLeftGroup = g.append("g")
    .attr("class", "y-left axis axisSteelBlue");

var yAxisRightGroup = g.append("g")
    .attr("class", "y-right axis barsFill")
    .attr("transform", "translate( " + width + ", 0 )");

// Get the data
d3.csv("static/js/data/top_50_goal_scorers.csv", function(error, data) {
  if (error) throw error;

  // format the data
  data.forEach(function(d) {
      d.season_number = +d.season_number;
      d.goals = +d.goals;
      d.gamesPlayed = +d.gamesPlayed;
  });

  players = Array.from(new Set(data.map(function(d) { return d.skaterFullName; })));
  createOptionsList(players, "playerSelect");
  formattedData = data;

  update(formattedData);

});

$("#playerSelect")
  .on("change", function() {
    update(formattedData);
  });

function update(dataFull) {
  var value = $("#playerSelect").val();
  console.log(value);

  var data = dataFull.filter(function(d) {
    return d.skaterFullName == value;
  });

  // Scale the range of the data
  xBarScale.domain(data.map(function(d) { return d.season_number; }));
  xLineScale.domain(data.map(function(d) { return d.season_number; }));
  yBarScale.domain([0, d3.max(data, function(d) { return d.gamesPlayed; })])
      .nice();
  yLineScale.domain([0, d3.max(data, function(d) { return d.goals; })])
      .nice();

  var rects = g.selectAll("rect")
      .data(data)

  rects.exit().remove();

  rects.enter().append("rect")
  	.merge(rects)
      .style("stroke", "none")
      .attr("class", "bar barsFill")
      .style("fill", "#82E0AA")
      .attr("x", function(d){ return xBarScale(d.season_number); })
      .attr("width", function(d){ return xBarScale.bandwidth(); })
      .attr("height", function(d){ return height - yBarScale(d.gamesPlayed); })
      .attr("y", function(d){ return yBarScale(d.gamesPlayed); });

  g.select(".line").remove();

  // Add the valueline path.
  g.append("path")
      .attr("class", "line")
      .style("stroke", "steelblue")
      .attr("d", valueline(data));

  var points1 = g.selectAll("circle.point1")
      .data(data);

  points1.exit().remove();

  points1.enter().append("circle")
  	.merge(points1)
      .attr("class", "point1")
      .style("stroke", "steelblue")
  		.style("fill", "steelblue")
      .attr("cx", function(d){ return xLineScale(d.season_number); })
      .attr("cy", function(d){ return yLineScale(d.goals); })
      .attr("r", function(d){ return 5; });


  // Add the X Axis
  var xAxisCall = d3.axisBottom(xLineScale);
  xAxisGroup.call(xAxisCall)

  // Add the left y-axis
  var yAxisLeftCall = d3.axisLeft(yLineScale);
  yAxisLeftGroup.call(yAxisLeftCall)
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", 6)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Goals");

  // Add the right y-axis
  var yAxisRightCall = d3.axisRight(yBarScale);
  yAxisRightGroup.call(yAxisRightCall)
      .call(d3.axisRight(yBarScale))
        .append("text")
          .attr("transform", "rotate(-90)")
          .attr("y", -12)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .text("Games Played");
}

function createOptionsList(items, id) {
  var str = ""
  for (var item of items) {
    str += "<option>" + item + "</option>"
  }
  document.getElementById(id).innerHTML = str;
}
