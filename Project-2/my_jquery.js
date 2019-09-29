$(document).ready(function(){
	


//tornado webserver

	var ws;
	var host = "localhost";
	var port = "8888";
	var uri = "/ws";

 	 // create websocket instance
 	 ws = new WebSocket("ws://" + host + ":" + port + uri);

 	 // Handle incoming websocket message callback
 	 ws.onmessage = function(evt) {
 	 	var temp = evt.data;
 	 	$("#output-temp").val(temp);
 	 };

 	 // Close Websocket callback
 	 ws.onclose = function(evt) {
 	 };

 	 // Open Websocket callback
  	ws.onopen = function(evt) { 
  	};	

	$(".get-temperature").click(function() {
		//$("#output-temp").val("400");
		ws.send("500").val();
	});



});
