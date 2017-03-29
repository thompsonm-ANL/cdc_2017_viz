function teamGraph(team_num) {
  window.graphs = new Array();
  d3.csv("state.csv", function(error, data) {

    points = []
    data.forEach(function(d) {
      if (d.num == team_num) {
        points.push({x: 1, y: parseInt(d.user)},
                    {x: 2, y: parseInt(d.attacker)},
                    {x: 3, y: parseInt(d.defender)})
      }
      exploder(team_num, d.attacker);
    });

    var options = {
      axisX: {
        tickLength: 0,
        lineThickness: 0,
        labelFontSize: 0,

      },
      axisY: {
        maximum: 1100,
        tickLength: 0,
        lineThickness: 0,
        labelFontSize: 0,
      },
      width:200,
      height:50,

      data: [{
        type: "bar",
        dataPoints: points
      }]
    }
    var divid = "g"+team_num;

    window.graphs[team_num] = new CanvasJS.Chart(divid, options);
  });
}

function updateGraph(team_num) {
  try {
    d3.csv("state.csv", function(error, data) {
      points = []
      data.forEach(function(d) {
        if (d.num == team_num) {
          points.push({x: 1, y: parseInt(d.user)},
                      {x: 2, y: parseInt(d.attacker)},
                      {x: 3, y: parseInt(d.defender)})
        }
        exploder(team_num, d.attacker);
      });
      divid = "#g"+team_num;
      window.graphs[team_num].options.data.dataPoints = points;
      window.graphs[team_num].render();
    });
  } catch(err) {
    console.log("couldn't read csv");
  }
}

function exploder(team_num, attacker) {
      var divid = "td"+team_num+" .explode";
  if (attacker > 900) {
    $(divid).show();
  } else {
    $(divid).hide();
  }
}
