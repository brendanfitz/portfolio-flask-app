var margin = { left:80, right:20, top:50, bottom:100 };

var width = 600 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var g = d3.select("#chart-area")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left + ", " + margin.top + ")");

var formattedData;
var xAxisGroup = g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height +")")

var yAxisGroup = g.append("g")
    .attr("class", "y axis")

// X Scale
var x = d3.scaleBand()
    .range([0, width])
    .padding(0.2);

// Y Scale
var y = d3.scaleLinear()
    .range([height, 0]);

// X Label
g.append("text")
    .attr("y", height + 90)
    .attr("x", width / 2)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Genre");

// Y Label
g.append("text")
    .attr("y", -60)
    .attr("x", -(height / 2))
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .attr("transform", "rotate(-90)")
    .text("Return on Investment");

d3.csv("/static/js/data/genre_roi.csv").then(function(data){
    // console.log(data);

    // Clean data
    data.forEach(function(d) {
        d.roi_total = +d.roi_total;
        d.roi_2018 = +d.roi_2018;
        d.roi_2017 = +d.roi_2017;
        d.roi_2016 = +d.roi_2016;
        d.roi_2015 = +d.roi_2015;
        d.roi_2014 = +d.roi_2014;
        d.roi_2013 = +d.roi_2013;
        d.roi_2012 = +d.roi_2012;
        d.roi_2011 = +d.roi_2011;
        d.roi_2010 = +d.roi_2010;
        d.roi_2009 = +d.roi_2009;
        d.roi_2008 = +d.roi_2008;
    });
    formattedData = data;

    update(data);
});

$("#yearSelect")
  .on("change", function() {
    update(formattedData);
  })

function update(data) {
    var value = $("#yearSelect").val();
    data.sort(function(a, b) {
        return b[value] - a[value];
     });
    // X Scale
    x.domain(data.map(function(d){ return d.genre }));
    y.domain([0, d3.max(data, function(d) { return d[value] })]);

    // X Axis
    var xAxisCall = d3.axisBottom(x);
    xAxisGroup.call(xAxisCall)
      .selectAll("text")
        .attr("transform", "rotate(-45)")
        .style("text-anchor", "end");

    // Y Axis
    var yAxisCall = d3.axisLeft(y)
        .tickFormat(function(d){ return d * 100 + '%'; });
    yAxisGroup.call(yAxisCall);

    // Bars
    var rects = g.selectAll("rect")
        .data(data);

    rects.exit().remove();

    rects.enter()
        .append("rect")
            .attr("y", function(d){ return y(d[value]); })
            .attr("x", function(d){ return x(d.genre) })
            .attr("height", function(d){ return height - y(d[value]); })
            .attr("width", x.bandwidth)
            .attr("fill", "grey")
            // And update old elements present in new data
            .merge(rects)
              .attr("x", function(d){ return x(d.genre) })
              .attr("width", x.bandwidth)
              .attr("y", function(d){ return y(d[value]); })
              .attr("height", function(d){ return height - y(d[value]); });
}
