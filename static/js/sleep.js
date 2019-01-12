


var sleepDisp = function() {
  var hrdrop = document.getElementById("hours");
  var hrchoice =  hrdrop.options[hrdrop.selectedIndex].value;
  //console.log(hrchoice);

  var mindrop = document.getElementById("minutes")
  var minchoice =  mindrop.options[mindrop.selectedIndex].value;

  var time = document.getElementById("time")

  var write = document.getElementById("display");
  write.innerHTML = hrchoice + ":" + minchoice + time.text;
};




var but = document.getElementById("x");
but.addEventListener('click', sleepDisp);
