


var pieChart = new PieChart('#chart-area');

d3.csv("static/js/data/outlays_by_function_2020.csv").then(function(data) {
  var dataClean = {}
  data.forEach(function(d) { dataClean[d.function] = +d.amount; })
  pieChart.wrangleData(dataClean);
})
