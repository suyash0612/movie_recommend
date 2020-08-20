

// working
// $(document).ready(function (){
//     $("#reviewer").click(function (){
//         $.ajax({
//             url:"http://192.168.0.106:8000/test/request_data",
//             datatype:"html",
//             type: "GET",
//             success: function(data) {
//                 $('#add_on').html(data);
//             }
            
//         });
//           });
//         });

$('#add_on').hide();
$('#add_in').hide();



$(document).ready(function(){
    $("#reviewer").click(function(){ 
        $('#load1').show();
        $('#add_in').hide();
        
        $.get({
            url: 'request_data/',
            success: function(data) {
                $('#load1').hide();
                $('#add_on').show();
                $('#add_on').html(data);
                

            }
        });
    });
});

$(document).ready(function(){
    $("#recommender").click(function(){ 
        $('#load1').show();
        $('#add_on').hide();
        
        $.get({
            url: 'request_choice/',
            success: function(data) {
                $('#add_in').show();
                $('#load1').hide();
                $('#add_in').html(data);

    
            }
            
        });
    });
});




var mybutton = document.getElementById("myBtn");

// When the user scrolls down 20px from the top of the document, show the button
window.onscroll = function() {scrollFunction()};

function scrollFunction() {
  if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
    mybutton.style.display = "block";
  } else {
    mybutton.style.display = "none";
  }
}

// When the user clicks on the button, scroll to the top of the document
function topFunction() {
  document.body.scrollTop = 0;
  document.documentElement.scrollTop = 0;
}




