/*
*    yield_curve.js
*/

var margin = { left:80, right:100, top:50, bottom:100 },
    height = 500 - margin.top - margin.bottom,
    width = 800 - margin.left - margin.right;

var svg = d3.select("#chart-area")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
var g = svg.append("g")
        .attr("transform", "translate(" + margin.left +
            ", " + margin.top + ")");

var t = function(){ return d3.transition().duration(1000); }

var parseTime = d3.timeParse("%m/%d/%Y");
var formatTime = d3.timeFormat("%m/%d/%Y");
var bisectDate = d3.bisector(function(d) { return d.date; }).left;

// Add the line for the first time
g.append("path")
    .attr("class", "line")
    .attr("fill", "none")
    .attr("stroke", "grey")
    .attr("stroke-width", "3px");

// Labels
var xLabel = g.append("text")
    .attr("class", "x axisLabel")
    .attr("y", height + 50)
    .attr("x", width / 2)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Instrument");
var yLabel = g.append("text")
    .attr("class", "y axisLabel")
    .attr("transform", "rotate(-90)")
    .attr("y", -60)
    .attr("x", -170)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Yield")

// Scales
treasurys_ord = [
  "1 Month", "2 Month", "3 Month", "6 Month", "1 Year",
  "2 Year", "3 Year", "5 Year", "7 Year", "10 Year", "20 Year", "30 Year"
]
var x = d3.scaleBand().domain(treasurys_ord).rangeRound([0, width]).padding(0.1),
    y = d3.scaleLinear().domain([0, 4]).rangeRound([height, 0]);

// X-axis
var xAxisCall = d3.axisBottom()
    .scale(x);
var xAxis = g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height +")")
    .call(xAxisCall);

// Y-axis
var yAxisCall = d3.axisLeft()
    .scale(y);
var yAxis = g.append("g")
    .attr("class", "y axis")
    .call(yAxisCall);

// Add jQuery UI slider
$("#date-slider").slider({
    min: parseTime("1/1/2020").getTime(),
    max: parseTime("3/5/2020").getTime(),
    step: 86400000, // One day
    slide: function(event, ui){
        $("#dateLabel").text(formatTime(new Date(ui.value)));
        update();
    }
});

d3.json("/api/yield_curve/2020").then(function(data){
    // Prepare and clean data
    formattedData = {};
    data.forEach((itemObj, i) => {
      var entryList = [];
      treasurys_ord.forEach((instrument, i) => {
          var entry = {};
          entry['instrument'] = instrument;
          entry['yield'] = +itemObj[instrument];
          entryList.push(entry);
      });
      formattedData[new Date(itemObj["Date"])] = entryList;
    });

    // Run the visualization for the first time
    update();
})

function update() {
    // Filter data based on selections
    //var sliderDate = $("#date-slider").slider("values");
    var sliderDate = new Date("3/5/2020");
    var data = formattedData[sliderDate];

    // Path generator
    line = d3.line()
        .x(function(d){ return x(d.instrument) + 22.5; })
        .y(function(d){ return y(d.yield); });

    // Update our line path

   g.select(".line")
     .transition(t)
     .attr("d", line(data));

   g.selectAll("circle")
       .data(data)
     .enter().append("circle")
       .attr("class", "circle")
       .attr("cx", function(d) { return x(d.instrument) + 22.5; })
       .attr("cy", function(d) { return y(d.yield); })
       .attr("r", 4)
}
