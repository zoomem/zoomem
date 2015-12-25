$("#next").on("click", function() {
  var number = $('#step');
  var data = 'step=' + number.val();
  $.ajax({
    url: "/visualize/next",
    data:data,
    context: document.body,
     success: function(data) {
      updatePage(data);
     }
   })
});

$("#prev").on("click", function() {
  var number = $('#step');
  var data = 'step=' + number.val();

  $.ajax({
    url: "/visualize/prev",
    data:data,
    context: document.body,
     success: function(data) {
       updatePage(data);
     }
   })
});

var cppEditor = CodeMirror.fromTextArea(document.getElementById("cpp-code"), {
  lineNumbers: true,
  matchBrackets: true,
  mode: "text/x-c++src",
  readOnly: true
});

function updatePage(json){
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
 }
