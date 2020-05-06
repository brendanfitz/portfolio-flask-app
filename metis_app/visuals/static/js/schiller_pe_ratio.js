
var margin = {top: 10, right: 30, bottom: 30, left: 60},
    width = 800 - margin.left - margin.right,
    height = 400 - margin.top - margin.bottom;

var svg = d3.select("#chart-area")
  .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom);

var g = svg.append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

//Read the data
d3.json("/api/schiller_pe_ratio", function(data) {

    // clean data
    data = data.map(function(d) {
      d['Schiller PE Ratio'] = +d['Schiller PE Ratio'];
      d.Date = Date.parse(d.Date);
      return d;
    });

    // Add X axis --> it is a date format
    var x = d3.scaleTime()
      .domain(d3.extent(data, function(d) { return d.Date; }))
      .range([ 0, width ]);

    g.append("g")
      .attr("transform", "translate(0," + height + ")")
      .call(d3.axisBottom(x).tickSizeOuter(0));

    // Add Y axis
    var y = d3.scaleLinear()
      .domain([0, d3.max(data, function(d) { return d['Schiller PE Ratio']; })])
      .range([ height, 0 ]);

    g.append("g")
      .call(d3.axisLeft(y).tickSizeOuter(0));

    var line = d3.line()
        .x(function(d) { return x(d.Date) })
        .y(function(d) { return y(d['Schiller PE Ratio']) });
    // Add the line
    g.append("path")
      .datum(data)
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", line)

})
