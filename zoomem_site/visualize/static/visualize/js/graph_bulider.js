var redraw;
function drawGraph(edges) {
    var width = $(document).width();
    var height = $(document).height() - 100;
    width /= 1.5;
    height /= 1.5;
    var render = function(r, n) {
            var set = r.set().push(
                r.rect(n.point[0]-30, n.point[1]-13, 60, 60).attr({ })).push(
                r.text(n.point[0], n.point[1] + 15,n.id + "\n" + n.name + "\n" + n.type + "\n" + n.value + "\n"));
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
      var src = edges[i][0]
      var tar = edges[i][1]
      var node = g.addNode(tar,{render:render});
      node.name = edges[i][2];
      node.address = edges[i][3]
      node.type = edges[i][4]
      node.size = edges[i][5]
      node.value = edges[i][6]
      node.flags =  edges[i][7]
      if(src != 1)
        edge = g.addEdge(src,tar);
    }

    var layouter = new Graph.Layout.Spring(g);
    var renderer = new Graph.Renderer.Raphael('drawArea', g, width, height);
    redraw = function() {
        layouter.layout();
        renderer.draw();
    };
}
