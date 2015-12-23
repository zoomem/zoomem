var redraw;
function drawGraph(edges,width) {

    $("#drawArea").empty();
    var height = width;
    var render = function(r, n) {
            var set = r.set().push(
                r.rect(n.point[0]-30, n.point[1]-13, 60, 60).attr({ })).push(
                r.text(n.point[0], n.point[1] + 15,n.id + "\n" + n.name + "\n" + n.type + "\n" + n.value + "\n"));
            return set;
        };

    var render = function(r, n) {
                /* the Raphael set is obligatory, containing all you want to display */
                var set = r.set().push(
                    /* custom objects go here */
                    r.rect(n.point[0]-30, n.point[1]-13, 62, 66)).push(
                    r.text(n.point[0], n.point[1] + 15,n.name).attr({"font-size":"14px"}));
                /* custom tooltip attached to the set */
                set./*tooltip = Raphael.el.tooltip;*/items.forEach(function(el) {
                  el.tooltip(r.set().push(r.text(25, 35, "type "+  n.type + "\n" + "val "+  n.value + "\n").attr({"font-size":"14px"})))});

    //            set.tooltip(r.set().push(r.rect(0, 0, 30, 30).attr({"fill": "#fec", "stroke-width": 1, r : "9px"})).hide());
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
