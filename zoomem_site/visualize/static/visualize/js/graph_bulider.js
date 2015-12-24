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
    border:"#b0bea3",
    boxbg:"#edf0ea",
    typebg:"#fafbfa",
    titlebg:"#748a61",
    font:"#748a61",
  },
  { // green
    border:"#9da7c4",
    boxbg:"#e9ebf1",
    typebg:"#f9fafb",
    titlebg:"#586792",
    font:"#586792",
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
}
function fillText(text,x,y,w){
  if(ctx.measureText(text).width<=w){
    ctx.fillText(text,x,y);
    return;
  }
  do{
    text=text.substr(0,text.length-2);
  }while(ctx.measureText(text+"...").width>w);
  ctx.fillText(text+"...",x,y);
}
Node.prototype.draw=function(){
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

  ctx.fillStyle=style[this.flag].font;
  fillText(this.value,this.x+3,this.y+50,this.w-8);
};
function drawEdge(x1,y1,x2,y2){
  ctx.lineWidth=2;
  ctx.beginPath();
  ctx.moveTo(x1,y1);
  ctx.bezierCurveTo(x2,y2,x1,y1,x2,y2);
  ctx.stroke();
}
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
var vis=[];
var tree=[];
function BFS(n){
  var q=[],f=0,l=-1;
  vis=[];
  tree=[];
  for(var i=0;i<n;++i){
    q.push(0);
    vis.push(0);
    tree.push([]);
  }
  vis[0]=1;
  q[++l]=0;
  while(f<=l){
    var u=q[f++];
    for(var i=0;i<adj[u].length;++i)
      if(vis[adj[u][i]]==0){
        vis[adj[u][i]]=1;
        tree[u].push(adj[u][i]);
        q[++l]=adj[u][i];
      }
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
    if(i+1<tree[u].length)
      y=DFS(tree[u][i],x+200,y);
    else {
      DFS(tree[u][i],x+200,y);
    }
    if(i+1<tree[u].length)
      y+=64;
  }
  y+=10;
  var lastY=y+56;
  if(nodes[u].flag==2){
    ctx.fillStyle=FRAMEBORDERCOLOR;
    ctx.fillRect(x+190-1,firstY-1,98+2,lastY-firstY+1+2);
    ctx.fillStyle=FRAMEBGCOLOR;
    ctx.fillRect(x+190,firstY,98,lastY-firstY+1);
  }
  y+=12;
  nodes[u].x=x;
  nodes[u].y=(nodes[tree[u][0]].y+nodes[tree[u][tree[u].length-1]].y)/2;
  if(nodes[u].flag==0){
    drawEdge(nodes[u].x+nodes[u].w-10,nodes[u].y+12,x+200-1,firstY+20);
  }else if(nodes[u].flag==2){
    drawEdge(nodes[u].x+nodes[u].w-10,nodes[u].y+12,x+190-1,(firstY+lastY)/2);
  }
  return y;
}
var first=1;
var dataEdges,dataN;
function drawGraph(edges,n) {
  if(first==1){
    dataEdges=edges;
    dataN=n;
    initialize();
    first=0;
  }
  nodes=[];
  adj=[];
  for(var i=0;i<n;++i){
    nodes.push(new Node({w:80,h:56,name:"-"}));
    adj.push([]);
  }
  for(var i=0;i<edges.length;++i){
    nodes[edges[i][1]-1].name=edges[i][2];
    nodes[edges[i][1]-1].flag=edges[i][7]-1;
    nodes[edges[i][1]-1].type=edges[i][4];
    nodes[edges[i][1]-1].value=edges[i][6];
    adj[edges[i][0]-1].push(edges[i][1]-1);
  }
  BFS(n);
  DFS(0,10,10);
  for(var i=1;i<n;++i)
    nodes[i].draw();
}
function draw(){
  updateCamera();
  ctx.clearRect(0,0,W,H);
  ctx.save();
  ctx.translate(cam.cx,cam.cy);
  ctx.scale(cam.cz,cam.cz);
  ctx.clearRect(0,0,W,H);
  drawGraph(dataEdges,dataN);
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
