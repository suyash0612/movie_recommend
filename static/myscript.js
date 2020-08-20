window.onload = testfunction;

var text;
function testfunction(){
text = document.getElementById('content');
text.onclick = search_text;

}

function search_text(){
  
  document.getElementById("l").style.display = "block";
  var name = document.getElementById("input_content").value;
  var req = new XMLHttpRequest();
  var url = "/test?name="+name;
  req.onreadystatechange = function() {
    if (this.readyState == 4 && this.status == 200) {
      location.replace(url)
    }


  };
  req.open("GET",url, true);
  req.send();
  
}



