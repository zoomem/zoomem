var cvs,ctx,W,H;
var NODEBGCOLOR="#ffffc6";
var NODEBORDERCOLOR="#AAA";
var nodes=[];
var adj=[];
var redraw;
function Node(o){
  this.x=o.x;
  this.y=o.y;
  this.w=o.w;
  this.h=o.h;
  this.name=o.name;
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
Node.prototype.draw=function(){
  ctx.fillStyle=NODEBGCOLOR;
  ctx.fillRect(this.x,this.y,this.w,this.h);
  ctx.lineWidth="1";
  ctx.strokeStyle=NODEBORDERCOLOR;
  ctx.strokeRect(this.x,this.y,this.w,this.h);
  ctx.beginPath();
  ctx.moveTo(this.x+6,this.y+23);
  ctx.lineTo(this.x+this.w-5,this.y+23);
  ctx.stroke();
  ctx.fillStyle="black";
  ctx.fillText(this.name,this.x+8,this.y+18);
};
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
  for(var i=0;i<tree[u].length;++i){
    y=DFS(tree[u][i],x+200,y);
    if(i+1<tree[u].length)
      y+=100;
  }
  y+=10;
  nodes[u].x=x;
  nodes[u].y=(nodes[tree[u][0]].y+nodes[tree[u][tree[u].length-1]].y)/2;
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
    nodes.push(new Node({x:Math.random()*500,y:Math.random()*500,w:80,h:90,name:"Hasan"}));
    adj.push([]);
  }
  for(var i=0;i<edges.length;++i){
    nodes[edges[i][1]-1].name=edges[i][2];
    adj[edges[i][0]-1].push(edges[i][1]-1);
  }
  BFS(n);
  DFS(0,10,10);
  for(var i=0;i<n;++i)
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
  ctx.fillText(cam.cx+" , "+cam.cy,100,100);
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
