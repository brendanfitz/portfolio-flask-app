


var dataClean = {}
var pieChart1 = new PieChart('#chart-area1');
var pieChart2 = new PieChart('#chart-area2');
var pieChart3 = new PieChart('#chart-area3');

d3.csv("static/js/data/outlays_by_function_2020.csv").then(function(data) {
  data.forEach(function(d) { dataClean[d.function] = +d.amount; })
  pieChart1.wrangleData(dataClean);
  pieChart2.wrangleData(dataClean);
  pieChart3.wrangleData(dataClean);
})

console.log(dataClean)
