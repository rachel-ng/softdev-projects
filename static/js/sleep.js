var sleepDisp = function() {
  var hrdrop = document.getElementById("hours");
  var hrchoice =  hrdrop.options[hrdrop.selectedIndex].value;
  //console.log(hrchoice);

  var mindrop = document.getElementById("minutes")
  var minchoice =  mindrop.options[mindrop.selectedIndex].value;

  //var time;
  var timechoice;
  if (document.getElementById('calc1').checked) {
    timechoice = 0
    //document.getElementById('o1').value;
  }
  else {
    timechoice = 1
    //document.getElementById('o2').value;
  }
  console.log("Time choice:" + timechoice);
  //console.log(timechoice)
  hourchoice = parseInt(hrchoice) + timechoice * 12;
  console.log(hourchoice);

  var ans = hourchoice.toString() + ":" + minchoice ;
  //console.log(ans);
  return ans;
};

var calcTime = function(n) {
  document.getElementById("sleepList").innerHTML = "";
  var start = Date.now();
  var end  = sleepDisp();
  var milliseconds = 90 * 60000; // 90 minutes

  var tmrw = new Date(start + 24 * 60 * 60 * 1000);
  var options = { year: 'numeric', month: 'numeric', day: 'numeric' };
  var tomorrow = tmrw.toLocaleDateString("en-US");
  var date2 = new Date(tomorrow + " " + end);
  var date3 = date2.getTime()- (15 * 60000);

  console.log(date2);
  console.log(date3);

  console.log("start " + start);

  var x = [];
  while ( date3  - (90 * 60000) >= start ){

      date3 = date3 - (90 * 60000);
      var date = new Date(date3);
      console.log("date3 " + date);
      var hrmin = date.toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'});
      x.unshift(hrmin);
  }
  console.log(x);

  var sleepTimes = document.getElementById("sleepList");
  var string = "";
  var numSleep = 0;
  var sleepGoal = x.length - 7
  // Button can be pressed multiple times resulting in the user being able to keep on appending the list
  // NEEDS TO BE FIXED
  for (var obj in x) {
    string += x[obj] + ", ";
    if (numSleep > sleepGoal) {
      var sleepTime = document.createElement("li");
      sleepTime.className = "list-group-item";
      sleepTime.innerHTML = x[obj];
      sleepTimes.appendChild(sleepTime);
    }
    numSleep++;
  }
  string = string.slice(0, -2);
  console.log(string);

  console.log("hello");
  return date3;
}



var but = document.getElementById("x");
but.addEventListener('click', calcTime);
