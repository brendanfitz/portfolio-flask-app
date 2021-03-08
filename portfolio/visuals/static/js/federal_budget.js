
/*
  Data source: https://www.cbo.gov/about/products/budget-economic-data#2
    Spending Projections
*/

var dorm_data = {};
var mandatory_data = {};
var discretionary_data = {};
var pieChart1 = new PieChart('#chart-area1', "Discretionary vs Mandatory Spending");
var pieChart2 = new PieChart('#chart-area2', "Mandatory Spending by Function");
var pieChart3 = new PieChart('#chart-area3', "Discretionary Spending by Function");

add_record = function(obj, d, key) {
  var record = {
    Allocation: +d.Allocation,
    Percent: +d.Percent
  }
  obj[d[key]] = record
}

d3.csv("static/js/data/Mandatory or Disc Budget Outlay Allocations (2020).csv").then(function(data) {
  data.forEach(function(d) { add_record(dorm_data, d, 'Discretionary or Mandatory'); });
  pieChart1.wrangleData(dorm_data);
})

d3.csv("static/js/data/Function Budget Outlay Allocations (2020).csv").then(function(data) {
  data.forEach(function(d) {
    if ((d['Discretionary or Mandatory'] == 'Mandatory') && (+d.Allocation > 0)) {
      add_record(mandatory_data, d, 'Function');
    }
  })
  pieChart2.wrangleData(mandatory_data);
  data.forEach(function(d) {
    if ((d['Discretionary or Mandatory'] == 'Discretionary') && (+d.Allocation > 0)) {
      add_record(discretionary_data, d, 'Function');
    }
  })
  pieChart3.wrangleData(discretionary_data);
})
