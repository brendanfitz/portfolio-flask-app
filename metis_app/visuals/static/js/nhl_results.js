/* Utility functions */
function addDays(date, days) {
    const copy = new Date(Number(date))
    copy.setDate(date.getDate() + days)
    return copy
}

function pad(s, maxlength) {
  var pad_length = maxlength - s.length;
  var padded_str = '&nbsp;'.repeat(pad_length) + s;
  return padded_str;
}

function dateDiff(start_date, end_date)   {
    //Get 1 day in milliseconds
    var one_day=1000*60*60*24;

    const diff_ms = Math.abs(end_date - start_date);
    const diffDays = Math.round(diff_ms / one_day);
    return diffDays;
}

function step(){
    // At the end of our data, loop back
    time = (time < maxTime - 1) ? time+1 : 0;
    update(formattedData[time]);
}

/* Plot configuration */
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

var time, teamData, interval, formattedData, maxTime, formatDate, minDate, maxDate;

teamData = {};
formatDate = d3.timeFormat("%Y-%m-%d");

// Tooltip
var tip = d3.tip().attr('class', 'd3-tip')
    .html(function(d) {
          var text = "<strong>Team:</strong> <span class='team-tooltip'>" + pad(d.team, 28) + "</span><br>";
          text += "<strong>Game #:</strong> <span style='color:aqua'>" + pad(d.games_played.toString(), 9) + "</span><br>";
        text += "<strong>Points:</strong> <span style='color:aqua'>" + pad(d.points.toString(), 13) + "</span><br>";
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

d3.json("/api/nhl-team-data").then(function(data){
  console.log(data);
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

d3.json("/api/nhl_results").then(function(data){
    maxTime = data.length;
    // Clean data
    formattedData = data.map(function(date){
        return date["teams"].map(function(team){
            team.games_played = +team.games_played;
            team.points = +team.points;
            return team;
        })
    });

    var dates = data.map(function(date) {
        return new Date(date['date']);
    })
    minDate=new Date(Math.min.apply(null,dates));
    maxDate=new Date(Math.max.apply(null,dates));

    // First run of the visualization
})
.then(create_controls)
.then(function() {
    time = maxTime - 1;
    update(formattedData[time]);
});

function create_controls() {
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
            time = 0;
            update(formattedData[time]);
        })
    
    $("#current-button")
        .on("click", function(){
            time = maxTime - 1;
            update(formattedData[time]);
        })
    
    $("#conference-select")
        .on("change", function(){
            update(formattedData[time]);
        })
    
    $("#division-select")
        .on("change", function(){
            update(formattedData[time]);
        })
    
    $("#wildcard-select")
        .on("change", function(){
            update(formattedData[time]);
        })
    
    $("#team-select")
        .on("change", function(){
            update(formattedData[time]);
        })
    
    $("#eastern-conference-wildcard-ref")
        .on("change", function(){
            update(formattedData[time]);
        })
    
    $("#western-conference-wildcard-ref")
        .on("change", function(){
            update(formattedData[time]);
        })
    
    $("#date-slider").slider({
        min: 0,
        max:  dateDiff(maxDate, minDate),
        step: 1,
        slide: function(event, ui){
            time = ui.value;
            update(formattedData[time]);
        }
    })
}

function update(data) {
    // Standard transition time for the visualization
    var t = d3.transition()
        .duration(100);

    // wildcard calcs
    var wildcard_bound_east = data.filter(function(d) {
      return d.wildcard == 'eastern';
    })[0].points;
    var wildcard_bound_west = data.filter(function(d) {
      return d.wildcard == 'western';
    })[0].points;

    var conference = $("#conference-select").val();
    var division = $("#division-select").val();
    var team = $("#team-select").val();
    var wildcard_race = $("#wildcard-select").val();
    var east_wildcard = $("#eastern-conference-wildcard-ref").is(":checked");
    var west_wildcard = $("#western-conference-wildcard-ref").is(":checked");

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
        if (wildcard_race == "all") { return true; }
        else {
            var rank_bool = d.division_rank > 3;
            var conf_bool = d.conference == wildcard_race;
            return (rank_bool && conf_bool);
        }
    });

    var data = data.filter(function(d){
        if (team == "all") { return true; }
        else {
            return team.includes(d.team);
        }
    });

    // JOIN new data with old elements.
    var logos = g.selectAll(".logos").data(data, function(d){
        return d.team;
    });

    // EXIT old elements not present in new data.
    logos.exit()
        .attr("class", "exit")
        .remove();

    // ENTER new elements present in new data.
    logos.enter()
        .append("image")
        .attr("class", "logos enter")
        .on("mouseover", tip.show)
        .on("mouseout", tip.hide)
        .attr("xlink:href", function(d) { return '/static/img/NHL-Logos/' + d.team + '.png' } )
        .attr("width", 25)
        .attr("height", 25)
        .attr("opacity", 0.7)
        .merge(logos)
        //.transition(t)
            .attr("x", function(d){ return x(d.games_played) })
            .attr("y", function(d){ return y(d.points) });

    // wildcard lines
    g.selectAll('line').remove();

    if (east_wildcard) {
        g.append('line')
            .attr('x1', x(0))
            .attr('y1', y(wildcard_bound_east))
            .attr('x2', x(82))
            .attr('y2', y(wildcard_bound_east))
            .attr('class', 'eastern-conference-wildcard');
    }

    if (west_wildcard) {
        g.append('line')
            .attr('x1', x(0))
            .attr('y1', y(wildcard_bound_west))
            .attr('x2', x(82))
            .attr('y2', y(wildcard_bound_west))
            .attr('class', 'western-conference-wildcard');
    }

    // Update the time label
    var dateString = formatDate(addDays(minDate, time));
    timeLabel.text(dateString);
    $("#game_date")[0].innerHTML = dateString;
    $("#date-slider").slider("value", +(time))
}
