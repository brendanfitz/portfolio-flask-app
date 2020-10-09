g = d3.select("#chart-area").append("svg")
    .attr("width", 850)
    .attr("height", 350)
    .attr("class", "wordcloud")
  .append("g")
    // without the transform, words words would get cutoff to the left and top, they would
    // appear outside of the SVG area
    .attr("transform", "translate(320,200)")

var fontSizeMin = 12,
    fontSizeMax = 48

function fontSizeGenerator(min, max) {
  return Math.random() * (max - min) + min;
}

colors = {
  gryffindor: "#740001",
  slytherin: "#1a472a",
  hufflepuff: "#ecb939",
  ravenclaw: "#0e1a40"
}

d3.json('/visuals/static/js/data/house_words.json', function(data) {

  frequency_lists = {};

  for (const house in data) {
    var frequency_list = [];
    data[house].map(function(word) {
      frequency_list.push({
        text: word,
        size: fontSizeGenerator(fontSizeMin, fontSizeMax)
      });
    })
    frequency_lists[house] = frequency_list;
  };

  update(frequency_lists);
});

$("#houseSelect")
  .on("change", function() {
    update(frequency_lists);
  });

function update(frequency_lists) {
  var house = $('#houseSelect').val();
  var frequency_list = frequency_lists[house];

  g.selectAll("text").remove();

  d3.layout.cloud().size([800, 300])
    .words(frequency_list)
    .rotate(0)
    .fontSize(function(d) { return d.size; })
    .on("end", draw)
    .start();

  function draw(words) {
    var texts = g.selectAll("text")
        .data(words);

    texts.enter().append("text")
        .style("font-size", function(d) { return d.size + "px"; })
        .style("fill", colors[house])
        .attr("transform", function(d) {
          return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
        })
        .text(function(d) { return d.text; });
  }
}
