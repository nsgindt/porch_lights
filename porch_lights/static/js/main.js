$(document).ready(function() {

/*    socket.on('my_response', function(msg) {
        $('#log').append('<br>' + $('<div>').text('Received #' + msg.count + ': ' + msg.data).html());
        $(".progress-bar").css("width", msg.data + "%");
        console.log( msg.data + "%");
    });

    socket.on('process_started', function(msg) {
        $('#processlog').append('<br>' + $('<div>').text(msg.data).html());
        $( "#startme" ).addClass( "disabled" ).prop('disabled', true);
        $( "#stopme" ).removeClass( "disabled" ).prop('disabled', false);
        if ($(".progress-bar").hasClass("bg-success")){
            $( ".progress-bar" ).removeClass( "bg-success" ).addClass( "bg-info" );
        }
        if ($(".progress-bar").hasClass("bg-danger")){
            $( ".progress-bar" ).removeClass( "bg-danger" ).addClass( "bg-info" );
        }
    });

    socket.on('process_stopped', function(msg) {
        $('#processlog').append('<br>' + $('<div>').text(msg.data).html());
        $( "#stopme" ).addClass( "disabled" ).prop('disabled', true);
        $( "#startme" ).removeClass( "disabled" ).prop('disabled', false);
    });

    socket.on('bot_complete', function(msg) {
        $('#processlog').append('<br>' + $('<div>').text(msg.data + ' @ ' + msg.time).html());
        $( "#stopme" ).addClass( "disabled" ).prop('disabled', true);
        $( "#startme" ).removeClass( "disabled" ).prop('disabled', false);
        $(".progress-bar").removeClass( "bg-info" ).addClass( "bg-success" );
    });

    socket.on('bot_aborted', function(msg) {
        $('#processlog').append('<br>' + $('<div>').text(msg.data + ' @ ' + msg.time).html());
        $( "#stopme" ).addClass( "disabled" ).prop('disabled', true);
        $( "#startme" ).removeClass( "disabled" ).prop('disabled', false);
        $(".progress-bar").removeClass( "bg-info" ).addClass( "bg-danger" );
    });

    socket.on('process_status', function(msg) {
        $('#process_status').html( 'step ' + msg.step + ' of ' + msg.total_steps);
    });

    $( "#stopme" ).click(function() {
      socket.emit('stopme');
    });
    $( "#startme" ).click(function() {
      socket.emit('startme');
    });
*/
   $( ".color-picker" ).click(function() {
      $('#color-option').val(this.id);
      console.log("red clicked");
    });

   $( ".pattern-picker" ).click(function() {
      $('#pattern-option').val(this.id);
      console.log("red clicked");
    });

    $( "#startme" ).click(function() {
        $color = $('#color-option').val();
        $pattern = $('#pattern-option').val();
        $url = "/start/"+$color + "/" + $pattern
      window.location.href = $url
    });

    $( "#stopme" ).click(function() {
        $url = "/stop"
      window.location.href = $url
    });

});            

/*$(document).on( "click", ".color-picker", function(ev) {

      $('#color-option').val(this.id);
      console.log("red clicked");
});*/