
PieChart = function(_parentElement) {
  this.parentElement = _parentElement;
  this.initVis();
};

PieChart.prototype.initVis = function() {
  var vis = this;

  // set the dimensions and margins of the graph
  vis.width = 600;
  vis.height = 600;
  vis.margin = 20;

  // The radius of the pieplot is half the width or half the height (smallest one). I subtract a bit of margin.
  vis.radius = Math.min(vis.width, vis.height) / 3 - vis.margin;

  // append the svg object to the div called 'my_dataviz'
  vis.svg = d3.select(vis.parentElement)
    .append("svg")
      .attr("width", vis.width)
      .attr("height", vis.height)
    .append("g")
      .attr("transform", "translate(" + vis.width / 2 + "," + vis.height / 2 + ")");
  // set the color scale
  vis.color = d3.scaleOrdinal()
    .range(d3.schemeDark2);

  // Compute the position of each group on the pie:
  vis.pie = d3.pie()
    .sort(null) // Do not sort group by size
    .value(function(d) { return d.value; })

  // The arc generator
  vis.arc = d3.arc()
    .innerRadius(vis.radius * 0.5)         // This is the size of the donut hole
    .outerRadius(vis.radius * 0.8)

  // Another arc that won't be drawn. Just for labels positioning
  vis.outerArc = d3.arc()
    .innerRadius(vis.radius * 0.9)
    .outerRadius(vis.radius * 0.9)
}

PieChart.prototype.wrangleData = function(_data) {
  var vis = this;

  // Create dummy data
  //vis.data = {a: 9, b: 20, c:30, d:8, e:12, f:3, g:7, h:14};
  vis.data = _data;
  vis.data_pie = vis.pie(d3.entries(vis.data));

  vis.updateVis();
};

PieChart.prototype.updateVis = function() {
  var vis = this;
  keys = this.data_pie.map(function(d) { return d.data.key; })
  vis.color.domain(keys);

  // Build the pie chart: Basically, each part of the pie is a path that we build using the arc function.
  vis.svg
    .selectAll('allSlices')
    .data(vis.data_pie)
    .enter()
    .append('path')
      .attr('d', vis.arc)
      .attr('fill', function(d){ return(vis.color(d.data.key)) })
      .attr("stroke", "white")
      .style("stroke-width", "2px")
      .style("opacity", 0.7)

  // Add the polylines between chart and labels:
  vis.svg
    .selectAll('allPolylines')
    .data(vis.data_pie)
    .enter()
    .append('polyline')
      .attr("stroke", "black")
      .style("fill", "none")
      .attr("stroke-width", 1)
      .attr('points', function(d) {
        var posA = vis.arc.centroid(d) // line insertion in the slice
        var posB = vis.outerArc.centroid(d) // line break: we use the other arc generator that has been built only for that
        var posC = vis.outerArc.centroid(d); // Label position = almost the same as posB
        var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2 // we need the angle to see if the X position will be at the extreme right or extreme left
        posC[0] = vis.radius * 0.95 * (midangle < Math.PI ? 1 : -1); // multiply by 1 or -1 to put it on the right or on the left
        return [posA, posB, posC]
      })

  // Add the polylines between chart and labels:
  vis.svg
    .selectAll('allLabels')
    .data(vis.data_pie)
    .enter()
    .append('text')
      .text( function(d) { return d.data.key } )
      .attr('transform', function(d) {
          var pos = vis.outerArc.centroid(d);
          var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
          pos[0] = vis.radius * 0.99 * (midangle < Math.PI ? 1 : -1);
          return 'translate(' + pos + ')';
      })
      .style('text-anchor', function(d) {
          var midangle = d.startAngle + (d.endAngle - d.startAngle) / 2
          return (midangle < Math.PI ? 'start' : 'end')
      })
      .style('font-size', '8px')

};
