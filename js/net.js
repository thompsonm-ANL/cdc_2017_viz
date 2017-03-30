window.lines = []

var colors = new Array();
for(col=0x0;col<=0xFFFFFF;col++) {
  colors.push("#" + col);
}
setTimeout( function() {
    id();
}, 6000);

setInterval(function() {

}, 10000);

function id() {
    $("line").each(function(index) {
        //$(this).css("stroke", colors[index*22]);
        $(this).attr("id", "l"+index);
    })
    $(".node").each(function(index) {
        //$(this).css("fill", colors[index*13]);
        $(this).attr("id", "n"+index);
    })
 }
