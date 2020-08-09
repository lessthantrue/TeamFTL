
var activeKey = undefined;
var rightbtn = false;

function sendKey(){
  console.log("Sending a thing!");
  xhr = new XMLHttpRequest();
  xhr.open('POST', "/keys/a");
  xhr.send()
}

function refresh(){
  console.log("Refreshing!");
  screensrc = document.getElementById('screen').getAttribute('src');
  document.getElementById('screen').setAttribute("src", screensrc + "?" + new Date().getTime())
}

setInterval(refresh, 2*1000);

function screenClick(evnt){
  x = evnt.pageX - this.offsetLeft;
  y = evnt.pageY - this.offsetTop;
  if(!this.classList.contains("nonadjusted")){
    x += 1152;
    y += 50;
  }
  xhr = new XMLHttpRequest();
  xhr.open('POST', '/mouse/'+x+'/'+y+'?key='+activeKey+"&r="+rightbtn);
  xhr.send();
}

function getSendKeyHandler(k, action, withClick, rightClick){
  return () => {
    if(action){
      console.log("Sending key " + k);
      xhr = new XMLHttpRequest();
      xhr.open('POST', '/keys/' + k);
      xhr.send();
    }
    if(withClick){
      activeKey = k;
    }
    else{
      activeKey = undefined;
    }
    rightbtn = rightClick;
  }
}

inputs = document.getElementsByClassName("ftl-input");
for(var i = 0; i < inputs.length; i++){
  inputs[i].addEventListener("click", getSendKeyHandler(inputs[i].id, !inputs[i].classList.contains("no-action"), inputs[i].classList.contains("with-click"), inputs[i].classList.contains("right")));
}

document.getElementById('screen').addEventListener('click', screenClick);

console.log("setup")
