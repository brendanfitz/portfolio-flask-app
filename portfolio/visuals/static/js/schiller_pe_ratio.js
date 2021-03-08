var lineChart;

//Read the data
d3.json("/api/schiller_pe_ratio", function(data) {

    // clean data
    data = data.map(function(d) {
      d['Schiller PE Ratio'] = +d['Schiller PE Ratio'];
      d.Date = Date.parse(d.Date);
      return d;
    });

    lineChart = new LineChart("#chart-area", data);
})
