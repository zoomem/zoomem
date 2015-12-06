var redraw;
function drawGraph(edges) {
    var width = $(document).width();
    var height = $(document).height() - 100;
    width /= 1.5;
    height /= 1.5;
    var render = function(r, n) {
            var set = r.set().push(
                r.rect(n.point[0]-30, n.point[1]-13, 60, 44).attr({"fill": "#feb", r : "12px", "stroke-width" : n.distance == 0 ? "3px" : "1px" })).push(
                r.text(n.point[0], n.point[1] + 10, (n.label || n.id) + "\n"));
            return set;
        };

    var g = new Graph();

    g.edgeFactory.build = function(source, target) {
    	var e = jQuery.extend(true, {}, this.template);
    	e.source = source;
    	e.target = target;
    	return e;
    }
    for(var i = 0; i < edges.length; ++i){
      var src = edges[i][1]
      var tar = edges[i][2]
      if(src == 1 || tar == 1){
        g.addNode(Math.max(src,tar),{render:render});
      }
      else {
        g.addEdge(src,tar);
      }
    }

    var layouter = new Graph.Layout.Spring(g);
    var renderer = new Graph.Renderer.Raphael('drawArea', g, width, height);
    redraw = function() {
        layouter.layout();
        renderer.draw();
    };
}
