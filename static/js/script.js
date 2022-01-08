var papers = document.getElementsByClassName('pdf');
var inputs = document.getElementsByClassName('coordinate-input');
var selectedinput = inputs[0];
var y = 0;
var selectedpage = papers[0]

function getXYpos(elm) {
  y = elm.offsetTop;
  elm = elm.offsetParent;
  while(elm != null) {
    y = parseInt(y) + parseInt(elm.offsetTop);
    elm = elm.offsetParent;
  }
  return {'yp':y};
}

function getCoords(e) {
  var xy_pos = getXYpos(this);
  if(navigator.appVersion.indexOf("MSIE") != -1) {
    var standardBody = (document.compatMode == 'CSS1Compat') ? document.documentElement : document.body;
    y = event.clientY + standardBody.scrollTop;
  }
  else {
    y = e.pageY;
  }
  y = y - xy_pos['yp'];
}

function makeSelected(e) {
  selectedinput = this
}

for(var j=0; j<inputs.length; j++) {
  if(inputs[j]) {
    inputs[j].onclick = makeSelected;
  }
}

for(var i=0; i<papers.length; i++) {
  if(papers[i]) {
    papers[i].onmousemove = getCoords;
    papers[i].onclick = function() {
      selectedinput.value = y;
    };
  }
}
