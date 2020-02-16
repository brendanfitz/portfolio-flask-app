d3.json('/static/js/data/house_words.json', function(data) {
  words = data['gryffindor'];

  var frequency_list = [];

  var fontSizeMin = 12,
      fontSizeMax = 48
  function fontSizeGenerator(min, max) {
    return Math.random() * (max - min) + min;
  }
  words.map(function(word) {
    frequency_list.push({
      text: word,
      size: fontSizeGenerator(fontSizeMin, fontSizeMax)
    });
  })

  d3.layout.cloud().size([800, 300])
    .words(frequency_list)
    .rotate(0)
    .fontSize(function(d) { return d.size; })
    .on("end", draw)
    .start();

  function draw(words) {
      d3.select("#chart-area").append("svg")
          .attr("width", 850)
          .attr("height", 350)
          .attr("class", "wordcloud")
        .append("g")
          // without the transform, words words would get cutoff to the left and top, they would
          // appear outside of the SVG area
          .attr("transform", "translate(320,200)")
          .selectAll("text")
          .data(words)
        .enter().append("text")
          .style("font-size", function(d) { return d.size + "px"; })
          .style("fill", "#740001")
          .attr("transform", function(d) {
              return "translate(" + [d.x, d.y] + ")rotate(" + d.rotate + ")";
          })
          .text(function(d) { return d.text; });
  }
});
