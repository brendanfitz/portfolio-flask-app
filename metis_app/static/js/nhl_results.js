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

var time = 0;
var interval;
var formattedData;
var maxTime;
var formatDate = d3.timeFormat("%Y-%m-%d")
var baseDate = new Date("2019-10-2");
function addDays(date, days) {
  const copy = new Date(Number(date))
  copy.setDate(date.getDate() + days)
  return copy
}

// Tooltip
var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
        var text = "<strong>Team:</strong> <span style='color:red;text-transform:capitalize'>" + d.team + "</span><br>";
        text += "<strong>Game Number:</strong> <span style='color:red'>" + d.games_played + "</span><br>";
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

d3.csv("/static/js/data/nhl_team_data.csv").then(function(data){
  teamData = {};
  data.forEach((item, i) => {
    teamData[item['team']] = {
      color: item['color'],
      conference: item['conference'],
      division: item['division']
    };
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
    .attr("font-size", "18px")
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

d3.json("/static/js/data/nhl_results.json").then(function(data){
    maxTime = data.length;
    // Clean data
    formattedData = data.map(function(date){
        return date["teams"].filter(function(team){
            return team.points;
        }).map(function(team){
            team.games_played = +team.games_played;
            team.points = +team.points;
            return team;
        })
    });

    // First run of the visualization
    update(formattedData[maxTime - 1]);

})

$("#play-button")
    .on("click", function(){
        var button = $(this);
        if (button.text() == "Play"){
            button.text("Pause");
            interval = setInterval(step, 150);
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

$("#conference-select")
    .on("change", function(){
        update(formattedData[time]);
    })

$("#division-select")
    .on("change", function(){
        update(formattedData[time]);
    })

$("#team-select")
    .on("change", function(){
        update(formattedData[time]);
    })

function dateCalc()   {
    date1 = new Date();
    date2 = baseDate;
    const diffTime = Math.abs(date2 - date1);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays - 3;
}

$("#date-slider").slider({
    max:  dateCalc(),
    min: 0,
    step: 1,
    slide: function(event, ui){
        time = ui.value;
        update(formattedData[time]);
    }
})

function step(){
    // At the end of our data, loop back
    time = (time < maxTime - 1) ? time+1 : 0;
    update(formattedData[time]);
}

function update(data) {
    // Standard transition time for the visualization
    var t = d3.transition()
        .duration(100);

    var conference = $("#conference-select").val();
    var division = $("#division-select").val();
    var team = $("#team-select").val();

    var data = data.filter(function(d){
        if (conference == "all") { return true; }
        else {
            return conference == teamData[d.team]['conference'];
        }
    });

    var data = data.filter(function(d){
        if (division == "all") { return true; }
        else {
            return division == teamData[d.team]['division'];
        }
    });

    var data = data.filter(function(d){
        if (team == "all") { return true; }
        else {
            return team.includes(d.team);
        }
    });

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
        .attr("fill", function(d) { return teamData[d.team]['color']; })
        .on("mouseover", tip.show)
        .on("mouseout", tip.hide)
        .merge(circles)
//        .transition(t)
            .attr("cy", function(d){ return y(d.points); })
            .attr("cx", function(d){ return x(d.games_played) })
            .attr("r", 8)
            .attr("opacity", 0.3);

    // Update the time label
    timeLabel.text(formatDate(addDays(baseDate, time)));
    $("#game_date")[0].innerHTML = formatDate(addDays(baseDate, time));
    //$("#game_date")[0].innerHTML = +(time);
    $("#date-slider").slider("value", +(time))
}
