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
*/
   $( ".color-picker" ).click(function() {
        $('#color-option').val(this.id);
        $('#color-option').trigger("change");
    });

   $( ".pattern-picker" ).click(function() {
      $('#pattern-option').val(this.id);
      $('#pattern-option').trigger("change");
    });

   $( ".color-one-picker" ).click(function() {
      $('#color-one-option').val(this.id);
      $('#color-one-option').trigger("change");
    });

   $( ".color-two-picker" ).click(function() {
      $('#color-two-option').val(this.id);
      $('#color-two-option').trigger("change");
    });

    $( ".color-three-picker" ).click(function() {
      $('#color-three-option').val(this.id);
      $('#color-three-option').trigger("change");
    });

    $( "#startme" ).click(function() {
      $color = $('#color-option').val();
      $pattern = $('#pattern-option').val();
      $color1 = $('#color-one-option').val();
      $color2 = $('#color-two-option').val();
      $color3 = $('#color-three-option').val();

      
      if ($color == "Rainbow" ){
        $url = "/start/"+$color + "/" + $pattern;
      } else if ($color== "Solid-Fade"){
        $url = "/start/"+$color + "/" + $pattern;
      } else if ($color== "One-Color"){
        $url = "/start/"+$color + "/" + $color1 + "/" + $pattern;
      } else if ($color=="Two-Color"){
        $url = "/start/"+$color + "/" + $color1 + "/" + $color2 + "/" + $pattern;        
      } else if ($color=="Three-Color"){
        $url = "/start/"+$color + "/" + $color1 + "/" + $color2 + "/" + $color3 + "/" + $pattern;          
      };
      window.location.href = $url
    });

    $( "#stopme" ).click(function() {
        $url = "/stop"
      window.location.href = $url
    });

    $( "#color-option" ).change(function() {
        $color = $("#color-option").val();
        if ($color == "Rainbow" ){
          hide_color_one();
          hide_color_two();
          hide_color_three();
        } else if ($color== "Solid-Fade"){
          hide_color_one();
          hide_color_two();
          hide_color_three();
        } else if ($color== "One-Color"){
          show_color_one();
          hide_color_two();
          hide_color_three();
        } else if ($color=="Two-Color"){
          show_color_one();
          show_color_two();
          hide_color_three();          
        } else if ($color=="Three-Color"){
          show_color_one();
          show_color_two();
          show_color_three();          
        };
    });

});            
/*        if ($(".progress-bar").hasClass("bg-success")){
            $( ".progress-bar" ).removeClass( "bg-success" ).addClass( "bg-info" );
        }*/

function hide_color_one(){
  if ($('#color-one').hasClass("d-none")){
  } else {
    $('#color-one').addClass( "d-none" );
  };
};

function show_color_one(){
  if ($('#color-one').hasClass("d-none")){
     $('#color-one').removeClass( "d-none" ); 
  };  
};

function hide_color_two(){
  if ($('#color-two').hasClass("d-none")){
  } else {
    $('#color-two').addClass( "d-none" );
  };
};

function show_color_two(){
  if ($('#color-two').hasClass("d-none")){
     $('#color-two').removeClass( "d-none" ); 
  };  
};
function hide_color_three(){
  if ($('#color-three').hasClass("d-none")){
  } else {
    $('#color-three').addClass( "d-none" );
  };
};

function show_color_three(){
  if ($('#color-three').hasClass("d-none")){
     $('#color-three').removeClass( "d-none" ); 
  };  
};




/*$(document).on( "click", ".color-picker", function(ev) {

      $('#color-option').val(this.id);
      console.log("red clicked");
});*/
