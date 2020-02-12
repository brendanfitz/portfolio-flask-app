//Width and height of map
var width = 960;
var height = 500;
scale = 1000;
var lowColor = '#2abc89'
var highColor = '#bc2a66'

// D3 Projection
var projection = d3.geoAlbersUsa()
  .translate([width / 2, height / 2]) // translate to center of screen
  .scale([scale]); // scale things down so see entire US

// Define path generator
var path = d3.geoPath() // path generator that will convert GeoJSON to SVG paths
  .projection(projection); // tell path generator to use albersUsa projection

var tip = d3.tip()
  .attr("class", "d3-tip")
  .html(function(d) {
    var text = "<strong>Country:</strong> <span style='color:red'>" + d.properties.name + "</span><br>";
    text += "<strong>Default Rate:</strong> <span style='color:red'>" + d3.format('.1%')(d.properties.default_rate) + "</span><br>";
    return text;
  })

//Create SVG element and append map to the SVG
var svg = d3.select("#map-chart-area")
  .append("svg")
  .attr("width", width)
  .attr("height", height);

svg.call(tip);

// Load in my states data!
d3.csv("/static/js/data/statesdata.csv", function(data) {
	var dataArray = [];
	for (var d = 0; d < data.length; d++) {
		dataArray.push(parseFloat(data[d].default_rate));
	}
	var minVal = d3.min(dataArray)
	var maxVal = 0.35//d3.max(dataArray)
	var ramp = d3.scaleLinear().domain([minVal,maxVal]).range([lowColor,highColor])

  // Load GeoJSON data and merge with states data
  d3.json("/static/js/data/us-states.json", function(json) {

    // Loop through each state data value in the .csv file
    for (var i = 0; i < data.length; i++) {

      // Grab State Name
      var dataState = data[i].state;

      // Grab data value
      var dataValue = data[i].default_rate;

      // Find the corresponding state inside the GeoJSON
      for (var j = 0; j < json.features.length; j++) {
        var jsonState = json.features[j].properties.name;

        if (dataState == jsonState) {

          // Copy the data value into the JSON
          json.features[j].properties.default_rate = dataValue;

          // Stop looking through the JSON
          break;
        }
      }
    }

    // Bind the data to the SVG and create one path per GeoJSON feature
    svg.selectAll("path")
      .data(json.features)
      .enter()
      .append("path")
      .attr("d", path)
      .style("stroke", "#fff")
      .style("stroke-width", "1")
      .style("fill", function(d) { return ramp(d.properties.default_rate) })
      .on("mouseover", tip.show)
      .on("mouseout", tip.hide);

		// add a legend
		var w = 70, h = 150;

		var key = d3.select("#map-chart-area")
			.append("svg")
			.attr("width", w)
			.attr("height", h)
			.attr("class", "legend");

		var legend = key.append("defs")
			.append("svg:linearGradient")
			.attr("id", "gradient")
			.attr("x1", "100%")
			.attr("y1", "0%")
			.attr("x2", "100%")
			.attr("y2", "100%")
			.attr("spreadMethod", "pad");

		legend.append("stop")
			.attr("offset", "0%")
			.attr("stop-color", highColor)
			.attr("stop-opacity", 1);

		legend.append("stop")
			.attr("offset", "100%")
			.attr("stop-color", lowColor)
			.attr("stop-opacity", 1);

		key.append("rect")
			.attr("width", w - 50)
			.attr("height", h)
			.style("fill", "url(#gradient)")
			.attr("transform", "translate(0,10)");

		var y = d3.scaleLinear()
			.range([h, 0])
			.domain([minVal, maxVal]);

		var yAxis = d3.axisRight(y)
        .tickFormat(d3.format('.0%'));

		key.append("g")
			.attr("class", "y axis")
			.attr("transform", "translate(41,10)")
			.call(yAxis)
  });
});
