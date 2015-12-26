var cvs,ctx,W,H;
var FRAMEBGCOLOR="#fffae7";
var FRAMEBORDERCOLOR="#e4d6a7";
var nodes=[];
var adj=[];
var redraw;
var style=[

  { // red
    border:"#c79999",
    boxbg:"#f2e8e8",
    typebg:"#fbf8f8",
    titlebg:"#985353",
    font:"#985353",
  },
  { // gray
    border:"#b1b1b1",
    boxbg:"#ededed",
    typebg:"#fafafa",
    titlebg:"#757575",
    font:"#757575",
  },
  { // blue
    border:"#9da7c4",
    boxbg:"#e9ebf1",
    typebg:"#f9fafb",
    titlebg:"#586792",
    font:"#586792",
  },
  { // green
    border:"#b0bea3",
    boxbg:"#edf0ea",
    typebg:"#fafbfa",
    titlebg:"#748a61",
    font:"#748a61",
    line:"#cfd8c7",
  },
];
function Node(o){
  this.x=o.x;
  this.y=o.y;
  this.w=o.w;
  this.h=o.h;
  this.name=o.name;
  this.flag=o.flag;
  this.type=o.type;
  this.value=o.value;
  this.members=[];
  this.rect1=null;
  this.rect2=null;
}
function fillText(text,x,y,w,right){
  if(ctx.measureText(text).width<=w){
    var offset=right?+w-ctx.measureText(text).width:0;
    ctx.fillText(text,x+offset,y);
    return;
  }
  do{
    text=text.substr(0,text.length-2);
  }while(ctx.measureText(text+"...").width>w);
  var offset=right?+w-ctx.measureText(text).width:0;
  ctx.fillText(text+"...",x+offset,y);
}
Node.prototype.draw=function(){
  this.h=37+this.members.length*17;
  if(this.flag!=2)
    this.h+=17;
  else
    this.h+=1;
  ctx.lineWidth="1";
  ctx.fillStyle=style[this.flag].border;
  ctx.fillRect(this.x-1,this.y-1,this.w+2,this.h+2);
  ctx.fillStyle=style[this.flag].boxbg;
  ctx.fillRect(this.x,this.y,this.w,this.h);

  ctx.fillStyle=style[this.flag].border;
  ctx.fillRect(this.x-1,this.y+21,this.w+2,16);
  ctx.fillStyle=style[this.flag].typebg;
  ctx.fillRect(this.x,this.y+22,this.w,14);

/*
  ctx.fillStyle=style[this.flag].border;
  ctx.fillRect(this.x-1,this.y+38,this.w+2,16);
  ctx.fillStyle=style[this.flag].typebg;
  ctx.fillRect(this.x,this.y+39,this.w,14);
*/

  ctx.fillStyle=style[this.flag].font;
  fillText(this.type,this.x+3,this.y+21+12,this.w-8);

  ctx.strokeStyle=style[this.flag].border;
  ctx.beginPath();
  ctx.moveTo(this.x-3,this.y+3);
  ctx.lineTo(this.x+this.w-15,this.y+3);
  ctx.lineTo(this.x+this.w-5,this.y+12);
  ctx.lineTo(this.x+this.w-15,this.y+18);
  ctx.lineTo(this.x-3,this.y+18);
  ctx.closePath();
  ctx.stroke();
  ctx.fillStyle=style[this.flag].titlebg;
  ctx.fill();
  ctx.fillStyle="#ffffff";
  fillText(this.name,this.x+3,this.y+14,this.w-16);

  /*ctx.fillStyle=style[this.flag].font;
  fillText(this.value,this.x+3,this.y+50,this.w-8);*/

  var curY=this.y+50;
  for(var i=0;i<this.members.length;++i){
    ctx.fillStyle=style[this.flag].font;
    fillText(nodes[this.members[i]].name,this.x+6,curY,this.w/2-11);
    fillText(nodes[this.members[i]].value,this.x+this.w/2+6,curY,this.w/2-11,true);
    if(i+1<this.members.length){
      ctx.fillStyle=style[this.flag].line;
      ctx.fillRect(this.x+5,curY+5,this.w-10,1);
    }
    curY-=17;
    ctx.fillStyle=style[this.flag].border;
    ctx.beginPath();
    ctx.moveTo(this.x,curY+11);
    ctx.lineTo(this.x+3,curY+14);
    ctx.lineTo(this.x,curY+17);
    ctx.closePath();
    ctx.fill();
    ctx.beginPath();
    ctx.moveTo(this.x+this.w,curY+11);
    ctx.lineTo(this.x+this.w-3,curY+14);
    ctx.lineTo(this.x+this.w,curY+17);
    ctx.closePath();
    ctx.fill();
    nodes[this.members[i]].rect2={x:this.x,y:curY+6,w:this.w,h:17};
    curY+=17*2;
  }
  this.rect1={x:this.x,y:this.y,w:this.w,h:this.h};
};
var cam = {
    x: 0,
    y: 0,
    cx: 0,
    cy: 0,
    z: 1,
    cz: 1,
};
var mouse = {
    down: false,
    x: 0,
    y: 0,
    last: { x: 0, y: 0 },
};
function updateCamera() {
    cam.cx += (cam.x - cam.cx) / 10;
    cam.cy += (cam.y - cam.cy) / 10;
    cam.cz += (cam.z - cam.cz) / 10;
}
function drawEdge(from,to,startColor,endColor){
  var x1,y1,x2,y2,bestDistance=1e18;
  for(var i=0;i<from.length;++i)
    for(var j=0;j<to.length;++j){
      var distance=Math.sqrt(Math.pow(from[i].x-to[j].x,2)+Math.pow(from[i].y-to[j].y,2));
      if(distance-1e-9<=bestDistance){
        bestDistance=distance;
        x1=from[i].x;
        y1=from[i].y;
        x2=to[j].x;
        y2=to[j].y;
      }
    }
  ctx.lineWidth=1.5;
  var gradient = ctx.createLinearGradient(x1,y1, x2, y2);
  gradient.addColorStop("0", startColor);
  gradient.addColorStop("0.35", startColor);
  gradient.addColorStop("0.5", "black");
  //gradient.addColorStop("1", endColor);
  ctx.strokeStyle=gradient;
  ctx.beginPath();
  ctx.moveTo(x1,y1);
  ctx.bezierCurveTo(x1+45,y1-35,x2+5,y2,x2,y2);
  ctx.stroke();
}
var vis=[];
var tree=[];
var cost=[];
var nodesInOrder=[];
function BFS(n){
  var q=[],f=0,l=-1;
  vis=[];
  tree=[];
  cost=[];
  nodesInOrder=[];
  for(var i=0;i<n;++i){
    q.push(0);
    vis.push(0);
    cost.push(0);
    tree.push([]);
  }
  vis[0]=1;
  q[++l]=0;
  cost[0]=0;
  while(f<=l){
    var u=q[f++];
    if(u!=0)
      nodesInOrder.push([u,cost[u]]);
    for(var i=0;i<adj[u].length;++i)
      if(vis[adj[u][i]]==0){
        if(cost[u]!=0 && nodes[adj[u][i]].flag!=1 && nodes[adj[u][i]].flag!=2 && nodes[adj[u][i]].name!="$")
          continue;
        vis[adj[u][i]]=1;
        cost[adj[u][i]]=cost[u]+1;
        tree[u].push(adj[u][i]);
        q[++l]=adj[u][i];
      }
  }
  for(var i=0;i<n;++i)
    if(nodes[i].name=="$"){
      vis[i]=true;
      nodesInOrder.push([i,4]);
    }
}
function DFS(u,x,y){
  if(tree[u].length==0){
    nodes[u].x=x;
    nodes[u].y=y;
    return y;
  }
  var firstY=y-10;
  for(var i=0;i<tree[u].length;++i){
    y=DFS(tree[u][i],x+200,y);
    if(i+1<tree[u].length)
      y+=64;
  }
  var lastY=y-10;
  if(nodes[u].flag==2){
    ctx.fillStyle=FRAMEBORDERCOLOR;
    ctx.fillRect(x+190-1,firstY-1,85+2,lastY-firstY+1+2);
    ctx.fillStyle=FRAMEBGCOLOR;
    ctx.fillRect(x+190,firstY,85,lastY-firstY+1);
  }
  y+=10;
  nodes[u].x=x;
  nodes[u].y=(nodes[tree[u][0]].y+nodes[tree[u][tree[u].length-1]].y)/2;

  return y;
}
var first=1;
var dataEdges,dataN;
function drawGraph(edges,n,new_data) {
  if(new_data == true)
    first = 1;
  if(first==1){
    var str = ""
    for(var i = 0 ;i<edges.length;i++ )
      str+=edges[i] + "\n";
    alert(str);
    dataEdges=edges;
    dataN=n;
    initialize();
    first=0;
  }
  edges=dataEdges;
  n=dataN;
  nodes=[];
  adj=[];
  for(var i=0;i<n;++i){
    nodes.push(new Node({w:150,h:56,name:"-"}));
    adj.push([]);
  }
  for(var i=0;i<edges.length;++i){
    nodes[edges[i][1]-1].name=edges[i][2];
    nodes[edges[i][1]-1].flag=edges[i][7]-1;
    nodes[edges[i][1]-1].type=edges[i][4];
    nodes[edges[i][1]-1].value=edges[i][6];
    adj[edges[i][0]-1].push(edges[i][1]-1);
  }
  for(var i=0;i<edges.length;++i){
    if(nodes[edges[i][0]-1].flag==2){
      nodes[edges[i][0]-1].members.push(edges[i][1]-1);
      //alert(edges[i][0] + " " + edges[i][1]);
      //alert((edges[i][0]-1) + " " + (edges[i][1]-1));
    }

  }
  BFS(n);
  vis[0]=false;
  /*DFS(0,10,10);
  for(var i=1;i<n;++i)
    if(vis[i]==1){
      nodes[i].draw();

    }*/
  var curX=10,curY=10;
  for(var i=0;i<nodesInOrder.length;++i){
    if(i>0 && nodesInOrder[i][1]!=nodesInOrder[i-1][1]){
      curY=10;
      curX+=200;
    }
    nodes[nodesInOrder[i][0]].x=curX;
    nodes[nodesInOrder[i][0]].y=curY;
    nodes[nodesInOrder[i][0]].draw();
    curY+=nodes[nodesInOrder[i][0]].h+10;
  }
  for(var i=0;i<edges.length;++i){
    var u=edges[i][0]-1;
    var v=edges[i][1]-1;
    if(u==0)
      continue;
    if(nodes[u].rect1==null && nodes[u].rect2==null)
      continue;
    if(nodes[v].rect1==null && nodes[v].rect2==null)
      continue;
    if(nodes[u].flag==0){
      var x1,y1,x2,y2;
      var options1=[];
      var options2=[];
      if(nodes[u].rect1!=null){
        x1=nodes[u].rect1.x;
        y1=nodes[u].rect1.y+12;
        options1.push({x:x1,y:y1});
        options1.push({x:x1+nodes[u].rect1.w,y:y1});
      }else{
        x1=nodes[u].rect2.x;
        y1=nodes[u].rect2.y+nodes[u].rect2.h/2;
        options1.push({x:x1,y:y1});
        options1.push({x:x1+nodes[u].rect2.w,y:y1});
      }
      if(nodes[v].rect1!=null){
        x2=nodes[v].rect1.x+nodes[v].rect1.w;
        y2=nodes[v].rect1.y+12;
        options2.push({x:x2,y:y2});
        options2.push({x:x2+nodes[v].rect1.w,y:y2});
      }else{
        x2=nodes[v].rect2.x;
        y2=nodes[v].rect2.y+nodes[v].rect2.h/2;
        options2.push({x:x2,y:y2});
        options2.push({x:x2+nodes[v].rect2.w,y:y2});
      }
      drawEdge(options1,options2,style[nodes[u].flag].titlebg,style[nodes[v].flag].titlebg);
    }
  }
  for(var i=1;i<nodes.length;++i)
    if(nodes[i].flag==2)
      for(var j=0;j<nodes[i].members.length;++j)
        if(nodes[nodes[i].members[j]].flag==2){
          var u=nodes[i].members[j];
          var x1,y1,x2,y2;
          if(nodes[u].rect1==null){
            alert(nodes[i].name+" ... idx = "+i+" ... other > "+nodes[u].name+" ... node = "+u+" .. type = "+nodes[u].type);
          }
          x1=nodes[u].rect2.x;
          y1=nodes[u].rect2.y+nodes[u].rect2.h/2;
          var options1=[{x:x1,y:y1},{x:x1+nodes[u].rect2.w,y:y1}];
          x2=nodes[u].rect1.x;
          y2=nodes[u].rect1.y+12;
          var options2=[{x:x2,y:y2},{x:x2+nodes[u].rect1.w,y:y2}];
          drawEdge(options1,options2,style[nodes[u].flag].titlebg,style[nodes[u].flag].titlebg);
      }
}
function draw(){
  updateCamera();
  ctx.clearRect(0,0,W,H);
  ctx.save();
  ctx.translate(cam.cx,cam.cy);
  ctx.scale(cam.cz,cam.cz);
  ctx.clearRect(0,0,W,H);
  drawGraph(dataEdges,dataN,false);
  ctx.restore();
  ctx.fillStyle="black";
  requestAnimationFrame(draw);
}
var done=0;
function initialize(){
  if(done==1)
    return;
  done=1;
  cvs=document.getElementById("cvs");
  ctx=cvs.getContext("2d");
  W=1280;
  H=720;
  cvs.onmousedown = function (e) {
      mouse.down = true;
      mouse.x = e.offsetX || (e.layerX-10);
      mouse.y = e.offsetY || (e.layerY-10);
      mouse.last = { x: mouse.x, y: mouse.y };
  };
  document.onmouseup = function (e) {
      mouse.down = false;
      mouse.last = { x: mouse.x, y: mouse.y };
  };
  document.onmousemove = function (e) {
    if (mouse.down == false)
        return;
    var x = e.clientX - cvs.offsetLeft;
    var y = e.clientY - cvs.offsetTop;
    cam.x += (x - mouse.x);
    cam.y += (y - mouse.y);
    mouse.x = x;
    mouse.y = y;
  };
  draw();
};
