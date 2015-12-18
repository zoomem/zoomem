$("#next").on("click", function() {
  var number = $('#step');
  var data = 'step=' + number.val();
  $.ajax({
    url: "/visualize/next",
    data:data,
    context: document.body,
     success: function(data) {
       $(document.body).html(data);
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
       $(document.body).html(data);
     }
   })
});

var cppEditor = CodeMirror.fromTextArea(document.getElementById("cpp-code"), {
  lineNumbers: true,
  matchBrackets: true,
  mode: "text/x-c++src",
  readOnly: true
});

function highlightLine(lineNumber) {
    var WRAP_CLASS = "CodeMirror-activeline";
    var BACK_CLASS = "CodeMirror-activeline-background";
       //Line number is zero based index
   var actualLineNumber = lineNumber - 1;
   var myEditor = $(".CodeMirror");
   console.log(myEditor);
   console.log(myEditor[0].CodeMirror);
   var codeMirrorEditor = myEditor[0].CodeMirror;
   codeMirrorEditor.addLineClass(actualLineNumber, "wrap", WRAP_CLASS);
   codeMirrorEditor.addLineClass(actualLineNumber, "background", BACK_CLASS);

   }
