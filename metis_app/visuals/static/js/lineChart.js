
LineChart = function(_parentElement, _data) {
  this.parentElement = _parentElement;
  this.data = _data
  this.initVis();
}

LineChart.prototype.initVis = function() {
  var vis = this;

  vis.margin = {top: 10, right: 30, bottom: 30, left: 60};
  vis.width = 800 - vis.margin.left - vis.margin.right,
  vis.height = 400 - vis.margin.top - vis.margin.bottom;

  vis.svg = d3.select(vis.parentElement)
    .append("svg")
      .attr("width", vis.width + vis.margin.left + vis.margin.right)
      .attr("height", vis.height + vis.margin.top + vis.margin.bottom);

  vis.g = vis.svg.append("g")
      .attr("transform", "translate(" + vis.margin.left + "," + vis.margin.top + ")");

  vis.x = d3.scaleTime()
    .domain(d3.extent(vis.data, function(d) { return d.Date; }))
    .range([ 0, vis.width ]);

  vis.y = d3.scaleLinear()
    .domain([0, d3.max(vis.data, function(d) { return d['Schiller PE Ratio']; })])
    .range([ vis.height, 0 ]);

  vis.updateVis();
}

LineChart.prototype.updateVis = function() {
  var vis = this;

  vis.g.append("g")
    .attr("transform", "translate(0," + vis.height + ")")
    .call(d3.axisBottom(vis.x).tickSizeOuter(0));

  vis.g.append("g")
    .call(d3.axisLeft(vis.y).tickSizeOuter(0));

  var line = d3.line()
    .x(function(d) { return vis.x(d.Date) })
    .y(function(d) { return vis.y(d['Schiller PE Ratio']) });

  vis.g.append("path")
    .datum(vis.data)
    .attr("fill", "none")
    .attr("stroke", "steelblue")
    .attr("stroke-width", 1.5)
    .attr("d", line)
}
