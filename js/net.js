window.lines = []

var colors = new Array();
for(col=0x0;col<=0xFFFFFF;col++) {
  colors.push("#" + col);
}
setTimeout( function() {
    id();
}, 6000);

setInterval(function() {
  updateLinks();
}, 10000);

function id() {
    window.l = new Map();
    $("line").each(function(index) {
        //$(this).css("stroke", colors[index*22]);
        var ourId = "l"+index;
        $(this).attr("id", ourId);
    })
    window.n = new Map()
    $(".node").each(function(index) {
        //$(this).css("fill", colors[index*13]);
        var ourId = "n"+index
        $(this).attr("id", ourId);
    })
 }

function updateLinks() {
  $.getJSON("/data", function(data) {
    data.forEach(function(d) {
      var thresholds = [200,400,600,800];
      $.getJSON("/lines", function(lines) {
        console.log("l "+lines[d.name]);
        if (d.attacker < thresholds[0]) {
          $("#"+lines[d.name]).css("stroke-width", "1");
        } else if (d.attacker >= thresholds[0] && d.attacker < thresholds[1]) {
          $("#"+lines[d.name]).css("stroke-width", "2");
        } else if (d.attacker >= thresholds[1] && d.attacker < thresholds[2]) {
          $("#"+lines[d.name]).css("stroke-width", "3");
          $("#"+lines[d.name]).css("stroke", "red");
        } else if (d.attacker >= thresholds[2] && d.attacker < thresholds[3]) {
          $("#"+lines[d.name]).css("stroke-width", "3");
          $("#"+lines[d.name]).css("stroke", "red");
        } else if (d.attacker >= thresholds[4]) {
          $("#"+lines[d.name]).css("stroke-width", "5");
          $("#"+lines[d.name]).css("stroke", "red");
        }
      })
    })
  })
}
