


var sleepDisp = function() {
  var hrdrop = document.getElementById("hours");
  var hrchoice =  hrdrop.options[hrdrop.selectedIndex].value;
  //console.log(hrchoice);

  var mindrop = document.getElementById("minutes")
  var minchoice =  mindrop.options[mindrop.selectedIndex].value;

  //var time;
  var timechoice;
  if (document.getElementById('o1').checked) {
    timechoice = document.getElementById('o1').value;
  }
  else {
    timechoice = document.getElementById('o2').value;
  }
  //console.log(time)
  console.log(timechoice)

  var write = document.getElementById("display");
  write.innerHTML = hrchoice + ":" + minchoice + time.text;
};




var but = document.getElementById("x");
but.addEventListener('click', sleepDisp);
