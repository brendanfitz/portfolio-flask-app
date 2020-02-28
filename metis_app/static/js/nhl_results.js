/*
*    main.js
*    Mastering Data Visualization with D3.js
*    6.7 - Adding a jQuery UI slider
*/

var margin = { left:80, right:20, top:50, bottom:100 };
var height = 500 - margin.top - margin.bottom,
    width = 800 - margin.left - margin.right;

var g = d3.select("#chart-area")
    .append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
    .append("g")
        .attr("transform", "translate(" + margin.left +
            ", " + margin.top + ")");

var time = 1;
var interval;
var formattedData;

// Tooltip
var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "<strong>Team:</strong> <span style='color:red;text-transform:capitalize'>" + d.team + "</span><br>";
        text = "<strong>Game Number:</strong> <span style='color:red'>" + d.game_number + "</span><br>";
        text += "<strong>Points:</strong> <span style='color:red'>" + d.points + "</span><br>";
        return text;
    });
g.call(tip);

// Scales
var x = d3.scaleLinear()
    .range([0, width])
    .domain([0, 84]);
var y = d3.scaleLinear()
    .range([height, 0])
    .domain([0, 100]);

d3.csv("/static/js/data/nhl_team_colors.csv").then(function(data){
  teamColors = {};
  data.forEach((item, i) => {
    console.log(teamColors);
    teamColors[item['team']] = item['color'];
  });
})

// Labels
var xLabel = g.append("text")
    .attr("y", height + 50)
    .attr("x", width / 2)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Game Number");
var yLabel = g.append("text")
    .attr("transform", "rotate(-90)")
    .attr("y", -40)
    .attr("x", -170)
    .attr("font-size", "20px")
    .attr("text-anchor", "middle")
    .text("Points")
var timeLabel = g.append("text")
    .attr("y", height -10)
    .attr("x", width - 40)
    .attr("font-size", "40px")
    .attr("opacity", "0.4")
    .attr("text-anchor", "middle")
    .text("1");

// X Axis
var xAxisCall = d3.axisBottom(x)
    .tickFormat(function(d){ return +d; });
g.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + height +")")
    .call(xAxisCall);

// Y Axis
var yAxisCall = d3.axisLeft(y)
    .tickFormat(function(d){ return +d; });
g.append("g")
    .attr("class", "y axis")
    .call(yAxisCall);
// var continents = ["europe", "asia", "americas", "africa"];
//
// var legend = g.append("g")
//     .attr("transform", "translate(" + (width - 10) +
//         "," + (height - 125) + ")");
//
// continents.forEach(function(continent, i){
//     var legendRow = legend.append("g")
//         .attr("transform", "translate(0, " + (i * 20) + ")");
//
//     legendRow.append("rect")
//         .attr("width", 10)
//         .attr("height", 10)
//         .attr("fill", continentColor(continent));
//
//     legendRow.append("text")
//         .attr("x", -10)
//         .attr("y", 10)
//         .attr("text-anchor", "end")
//         .style("text-transform", "capitalize")
//         .text(continent);
// });

d3.json("/static/js/data/nhl_results.json").then(function(data){
    // Clean data
    formattedData = data.map(function(game_number){
        return game_number["teams"].filter(function(team){
            return team.points;
        }).map(function(team){
            team.game_number = +team.game_number;
            team.points = +team.points;
            return team;
        })
    });

    // First run of the visualization
    update(formattedData[0]);

})

$("#play-button")
    .on("click", function(){
        var button = $(this);
        if (button.text() == "Play"){
            button.text("Pause");
            interval = setInterval(step, 250);
        }
        else {
            button.text("Play");
            clearInterval(interval);
        }
    })

$("#reset-button")
    .on("click", function(){
        time = 1;
        update(formattedData[0]);
    })

$("#team-select")
    .on("change", function(){
        update(formattedData[time]);
    })

$("#game-slider").slider({
    max: 82,
    min: 1,
    step: 1,
    slide: function(event, ui){
        time = ui.value;
        update(formattedData[time]);
    }
})

function step(){
    // At the end of our data, loop back
    time = (time < 82) ? time+1 : 1;
    update(formattedData[time]);
}

function update(data) {
    // Standard transition time for the visualization
    var t = d3.transition()
        .duration(100);

    var team = $("#team-select").val();

    var data = data.filter(function(d){
        if (team == "all") { return true; }
        else {
            return d.team == team;
        }
    })

    // JOIN new data with old elements.
    var circles = g.selectAll("circle").data(data, function(d){
        return d.team;
    });

    // EXIT old elements not present in new data.
    circles.exit()
        .attr("class", "exit")
        .remove();

    // ENTER new elements present in new data.
    circles.enter()
        .append("circle")
        .attr("class", "enter")
        .attr("fill", function(d) { return teamColors[d.team]; })
        .on("mouseover", tip.show)
        .on("mouseout", tip.hide)
        .merge(circles)
        .transition(t)
            .attr("cy", function(d){ return y(d.points); })
            .attr("cx", function(d){ return x(d.game_number) })
            .attr("r", 8)
            .attr("opacity", 0.3);

    // Update the time label
    timeLabel.text(+(time))
    $("#game_number")[0].innerHTML = +(time)

    $("#game-slider").slider("value", +(time))
}
