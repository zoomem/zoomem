
function disable_buttons(){
  $("input[type=button],:button").attr("disabled","disabled");
}
function enable_buttons()
{
  $("input[type=button],:button").removeAttr("disabled");
}
$("#next").on("click", function() {
  disable_buttons()
  var number = $('#step');
  var data = 'step=' + number.val();
  $.ajax({
    url: "/visualize/next",
    data:data,
    context: document.body,
     success: function(data) {
     if ( $( '#RuntimeError', $('<span/>').html( data ) ).length > 0 || $( '#TimeLimitError', $('<span/>').html( data ) ).length > 0)
     {
       document.open();
       document.write(data);
       document.close();
     }
     else {
       updatePage(data);
       enable_buttons();
     }

     },
     error: function(){
       enable_buttons();
     },
   })
});

$("#prev").on("click", function() {
  disable_buttons()
  var number = $('#step');
  var data = 'step=' + number.val();
  $.ajax({
    url: "/visualize/prev",
    data:data,
    context: document.body,
     success: function(data) {
       updatePage(data);
       enable_buttons();
     },
     error: function(){
       enable_buttons();
     },
   })
});

$("#end_funciton").on("click", function() {
  disable_buttons()
  $.ajax({
    url: "/visualize/end_funciton",
    context: document.body,
     success: function(data) {
       updatePage(data);
       enable_buttons();
     },
     error: function(){
       enable_buttons();
     },
   })
});

$("#stack_up").on("click", function() {
  disable_buttons()
  $.ajax({
    url: "/visualize/stack_up",
    context: document.body,
     success: function(data) {
       updatePage(data);
       enable_buttons();
     },
     error: function(){
       enable_buttons();
     },
   })
});

$("#stack_down").on("click", function() {
  disable_buttons()
  $.ajax({
    url: "/visualize/stack_down",
    context: document.body,
     success: function(data) {
       updatePage(data);
       enable_buttons();
     },
     error: function(){
       enable_buttons();
     },
   })
});

$("#edit").on("click", function() {
  window.location.href = '/?code=True';

});

$(".err-btn").on("click", function() {
  window.location.href = '/?code=True';
});

var cppEditor = CodeMirror.fromTextArea(document.getElementById("cpp-code"), {
  lineNumbers: true,
  matchBrackets: true,
  mode: "text/x-c++src",
  readOnly: true
});

function updatePage(json){
  var d = new Date();
  var n = d.getTime();
  highlightLine(json.line_num);
  $(".output").html(json.output);
  drawGraph(json.edges,json.cnt,true);
}

function highlightLine(lineNumber) {
  var BACK_CLASS = "CodeMirror-activeline-background";
  var actualLineNumber = lineNumber - 1;
  var myEditor = $(".CodeMirror");
  var codeMirrorEditor = myEditor[0].CodeMirror;
  for(var i=0; i<codeMirrorEditor.lineCount(); i++)
    codeMirrorEditor.removeLineClass(i,"background");
  codeMirrorEditor.addLineClass(actualLineNumber, "background", BACK_CLASS);
  jumpToLine(lineNumber,codeMirrorEditor);
 }

 function jumpToLine(i,editor) {
  var t = editor.charCoords({line: i, ch: 0}, "local").top;
  var middleHeight = editor.getScrollerElement().offsetHeight / 2;
  editor.scrollTo(null, t - middleHeight - 5);
}
