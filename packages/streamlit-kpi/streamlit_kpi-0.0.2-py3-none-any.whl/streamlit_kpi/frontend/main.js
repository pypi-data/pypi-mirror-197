// The `Streamlit` object exists because our html file includes
// `streamlit-component-lib.js`.
// If you get an error about "Streamlit" not being defined, that
// means you're missing that file.

function sendValue(value) {
  Streamlit.setComponentValue(value)
}

/**
 * The component's render function. This will be called immediately after
 * the component is initially loaded, and then again every time the
 * component gets new data from Python.
 */
function onRender(event) {
  const {height} = event.detail.args;
  const {title} = event.detail.args;
  const {value} = event.detail.args;
  const {icon} = event.detail.args;
  const {progress} = event.detail.args;
  const {animate} = event.detail.args;
  const {unit} = event.detail.args;
  const {animateDuration} = event.detail.args;
  const {showProgress}= event.detail.args;
  const {showIcon}=event.detail.args;
  const {iconTop}=event.detail.args;
  const {iconLeft}=event.detail.args;
  const {iconColor}=event.detail.args;
  const {iconOpacity}=event.detail.args;
  const {backgroundColor}=event.detail.args;
  const {titleColor}=event.detail.args;
  const {valueColor}=event.detail.args;
  const {progressColor}=event.detail.args;
  const {textAlign}=event.detail.args;
  
  Streamlit.setFrameHeight(height)
  document.querySelector(".card").style.height=height+"px"
  const titled = document.querySelector(".title span");
  const vald = document.querySelector(".card-content span");
  const icond = document.querySelector(".info-icon i");
  const pgb = document.querySelector(".progressbar");
  const iconParent=document.querySelector(".info-icon")
  const body=document.querySelector(".card")
  const text=document.querySelector(".header-row")
  text.style.textAlign=textAlign;
  vald.style.textAlign=textAlign;
  body.style.backgroundColor=backgroundColor;
  titled.style.color=titleColor;
  vald.style.color=valueColor;
  pgb.style.backgroundColor=progressColor;
  titled.innerHTML=title;
  

  if(isNaN(value)){
    vald.innerText=value;
    if(animate==true)
      animateText(vald,animateDuration)
  }
  else{
    oldVal=parseFloat(vald.innerText)
    if(animate==true)
      animateValue(vald,oldVal,value,animateDuration,unit)
    else
      vald.innerText=value  + unit
  }
  
  pgb.style.width=progress+"%";
  if(showProgress==false){
    pgb.style.display='none'
  }
  else[
    pgb.style.display=''
  ]
  if(showIcon==false){
    iconParent.style.display='none'
  }
  else{
    setTimeout(()=>{
    icond.className='fa'
    icon.split(' ').forEach(element => {
      icond.classList.add(element);
    });
    iconParent.style.display=''
    iconParent.style.top=(body.clientHeight*(iconTop/100)) - (icond.clientHeight/2) +'px'
    iconParent.style.left=(body.clientWidth*(iconLeft/100)) - (icond.clientWidth/2) +'px'
    icond.style.color=iconColor
    icond.style.opacity=iconOpacity/100
  },300)
  }
}

function animateText(elem,duration){
  lengthVal=elem.innerText.length;
  delay=(duration/lengthVal) - (duration/lengthVal)/3
  elem.innerHTML = elem.textContent.replace(/\S/g, '<div style="display: inline-block;" class="letter">$&</div>');
  anime.timeline({loop: false})
  .add({
    targets: '.letter',
    rotateY: [-90, 0],
    duration: duration,
    delay: (el, i) => delay * i
  })
}

function animateValue(elem, start, end, duration,unit) {
  var realEnd=end;
  var decimal = (realEnd+"").split(".")[1];
  end=parseInt(end)
  var obj = elem;
  var range = end - start;
  var minTimer = 50;
  var stepTime = Math.abs(Math.floor(duration / range));
  stepTime = Math.max(stepTime, minTimer);
  var startTime = new Date().getTime();
  var endTime = startTime + duration;
  var timer;
  function run() {
      var now = new Date().getTime();
      var remaining = Math.max((endTime - now) / duration, 0);
      var value = Math.floor(end - (remaining * range));
      var render=value +unit
      if(decimal)
        render=value+'.'+ padZero(getRandomInt(decimal),decimal.toString().length) +unit
      obj.innerHTML = render;
      if (value == end) {
          clearInterval(timer);
          obj.innerHTML = realEnd+unit;
      }
  }
  
  timer = setInterval(run, stepTime);
  run();
}

function getRandomInt(max) {
  return Math.floor(Math.random() * max);
}

function padZero(num, places){
  return String(num).padStart(places, '0')
}

Streamlit.events.addEventListener(Streamlit.RENDER_EVENT, onRender)
Streamlit.setComponentReady()
