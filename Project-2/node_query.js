$(document).ready(function(){

//nodejs webserver


	var ws;

 	 // create websocket instance

     ws = new WebSocket('ws://localhost:9898/ws');
	
	
	// Handle incoming websocket message callback
 	 ws.onmessage = function(evt) {
 	 	var temp = evt.data;
 	 	$("#output-temp-nodejs").val(temp);
 	 };
	 
 	 // Close Websocket callback
 	 ws.onclose = function(evt) {
 	 };
 	 
 	 
 	 ws.onopen = function(evt) {
		console.log('Hi this is web client.');
	};
 

	$(".get-temperature-nodejs").click(function() {
		ws.send("500").val();
	});

});
