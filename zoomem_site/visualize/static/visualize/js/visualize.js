$(".code_area").keydown(function(e) {
    if(e.keyCode === 9) { // tab was pressed
        var start = this.selectionStart;
        var end = this.selectionEnd;

        var $this = $(this);
        var value = $this.val();
        $this.val(value.substring(0, start)
                    + "\t"
                    + value.substring(end));

        this.selectionStart = this.selectionEnd = start + 1;
        e.preventDefault();
    }
});
