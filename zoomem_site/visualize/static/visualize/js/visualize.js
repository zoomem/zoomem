$("#next").on("click", function() {
  $.ajax({
    url: "/visualize/next",
    context: document.body,
     success: function(data) {
       $(document.body).html(data);
     }
   })
});

$("#prev").on("click", function() {
  $.ajax({
    url: "/visualize/prev",
    context: document.body,
     success: function(data) {
       $(document.body).html(data);
     }
   })
});

$("#first").on("click", function() {
  alert("pressed");
});

$("#last").on("click", function() {
  alert("pressed");
});

var cppEditor = CodeMirror.fromTextArea(document.getElementById("cpp-code"), {
  lineNumbers: true,
  matchBrackets: true,
  mode: "text/x-c++src",
  readOnly: true
});
