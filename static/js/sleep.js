var but = document.getElementById("x");
but.addEventListener('click', fibonacci);



var sleepCalc = function() {
  console.log("1");
  var hr = document.getElementById("hour");
  console.log(hr);
  console.log("hi");
};

var fibonacci = function(n) {
  //base case 1: the number is 0 -> return 0
	if ( n == 0 ) {
		return 0;
	}
  //base case 2: the number is 1 -> return 1
	if ( n == 1 ) {
		return 1;
	}
  //use recursion: find the n-1th and n-2th Fibonacci numbers and add them
	else {
		return fibonacci(n-1) + fibonacci(n-2);
	}
};

var displayfib = function() {
	var x = fibonacci(10);
	console.log(x);
}
