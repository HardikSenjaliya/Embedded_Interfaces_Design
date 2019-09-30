$(document).ready(function(){	
		
//nodejs webserver

	 var ws;

 	 // create websocket instance

     ws = new WebSocket('ws://localhost:9898/ws');
    

 	 ws.onmessage = function (evt) {
	 var hum = evt.data;
			
     $("#output-sql").val(hum);

 	 };
	 
	//Close websocket callback
 	 ws.onclose = function (evt) {
 	 }; 	 
 	 
	//open websocket callback
	 ws.onopen = function (evt) {
		
	};
	
	$(".get-last-sql").click(function () {
		ws.send("Get SQL").val();	

	});

});

