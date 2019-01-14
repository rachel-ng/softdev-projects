
var sleepDisp = function() {
  var hrdrop = document.getElementById("hours");
  var hrchoice =  hrdrop.options[hrdrop.selectedIndex].value;
  //console.log(hrchoice);

  var mindrop = document.getElementById("minutes")
  var minchoice =  mindrop.options[mindrop.selectedIndex].value;

  //var time;
  var timechoice;
  if (document.getElementById('o1').checked) {
    timechoice = 0
    //document.getElementById('o1').value;
  }
  else {
    timechoice = 1
    //document.getElementById('o2').value;
  }
  //console.log(timechoice)
  hourchoice = parseInt(hrchoice) + timechoice * 12;
  console.log(hourchoice)

  var ans = hourchoice.toString() + ":" + minchoice ;
  //console.log(ans);
  return ans;
};

var calcTime = function(n) {
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

  var string = "";
  for (var obj in x) {
    string += obj + ", "
  }
  string = string.slice(0, -2);
  console.log(string);

  var write = document.getElementById("display");
  write.innerHTML = string;
  return date3;
}



var but = document.getElementById("x");
but.addEventListener('click', calcTime);
