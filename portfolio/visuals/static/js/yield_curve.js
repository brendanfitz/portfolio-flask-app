/*
*    yield_curve.js
*/

var margin = { left:80, right:100, top:50, bottom:100 },
    height_wo_margins = 500,
    width_wo_margins = 1000,
    height = height_wo_margins - margin.top - margin.bottom,
    width = width_wo_margins - margin.left - margin.right;

var aspect_ratio_adjustment = 0.85;

for (const side in margin) {
    margin[side] = margin[side] * aspect_ratio_adjustment;
}
height = height_wo_margins * aspect_ratio_adjustment - margin.top - margin.bottom;
width = width_wo_margins * aspect_ratio_adjustment - margin.left - margin.right;

var svg = d3.select("#chart-area")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
var g = svg.append("g")
        .attr("transform", "translate(" + margin.left +
            ", " + margin.top + ")");

var t = function(){ return d3.transition().duration(1000); };

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
    .attr("y", -40)
    .attr("x", -140)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Yield (%)")

// Scales
treasurys_ord = [
  "1 Month", "2 Month", "3 Month", "6 Month", "1 Year",
  "2 Year", "3 Year", "5 Year", "7 Year", "10 Year", "20 Year", "30 Year"
]
var x = d3.scaleBand().domain(treasurys_ord).rangeRound([0, width]).padding(0.1),
    y = d3.scaleLinear().domain([0, 6]).rangeRound([height, 0]);

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

var formattedData = {};

d3.json("/api/yield_curve/202309").then(function(data){
    // Prepare and clean data
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

    dates = Object.keys(formattedData);

    $("#date-slider").slider({
        min: 0,
        max: dates.length - 1,
        value: dates.length - 1,
        step: 1, // One day
        slide: function(event, ui){
            var date = dates[ui.value];
            $("#dateLabel").text(formatTime(new Date(date)));
            update(date);
        }
    });

    // Run the visualization for the first time
    var date = dates.slice(-1)[0];
    $("#dateLabel").text(formatTime(new Date(date)));
    update(date);
})

function update(date) {
    // Filter data based on selections
    var data = formattedData[date];

    // Path generator
    line = d3.line()
        .x(function(d){ return x(d.instrument) + 22.5; })
        .y(function(d){ return y(d.yield); });

    // Update our line path

   g.select(".line")
     .transition(t)
     .attr("d", line(data));

}
