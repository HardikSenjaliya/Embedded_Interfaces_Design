$(document).ready(function(){
	
//tornado webserver

	var ws;
	var host = "10.0.0.193";
	var port = "8888";
	var uri = "/ws";

 	 // create websocket instance
 	 ws = new WebSocket("ws://" + host + ":" + port + uri);

 	 // Handle incoming websocket message callback
 	 ws.onmessage = function(evt) {
 	 	var rcvd_message = evt.data.split(',');

 	 	$("#output-vals-time").val(rcvd_message[1]);
 	 	$("#output-vals-temp").val(rcvd_message[2] + "C");
 	 	$("#output-vals-humi").val(rcvd_message[3] + "%");

 	 };

 	 // Close Websocket callback
 	 ws.onclose = function(evt) {
 	 };

 	 // Open Websocket callback
  	ws.onopen = function(evt) { 
  	};	

	$(".get-vals-tornado").click(function() {
		ws.send("Get Current Sensor Values").val();
	});
});
