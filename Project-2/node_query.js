$(document).ready(function(){	
		
//nodejs webserver
     
     var wsnj;
     var start_time_nj = 0;
     var end_time_nj = 0;
     var time_diff_nj = 0;
     var curr_unit=0;
    

	// create websocket instance

     wsnj = new WebSocket('ws://localhost:9898/ws');
     
     wsnj.onmessage = function (evt) {
	var dat = evt.data.split(',');
			
	if(dat[0] == "Get SQL"){
		$("#output-vals-time-nj").val(dat[1]);
		$("#output-vals-temp-nj").val(dat[2] + " C");
		$("#output-vals-humi-nj").val(dat[4] + " %");
	}

	else if(dat[0] == "Get Last NJS Ten Values"){
		$("#nj-start-time").val(start_time_nj.getHours()+":"+start_time_nj.getMinutes()+":"+start_time_nj.getSeconds());
		end_time_nj = new Date($.now());
 		time_diff_nj = end_time_nj.getTime() - start_time_nj.getTime();
		$("#nj-end-time").val(end_time_nj.getHours()+":"+end_time_nj.getMinutes()+":"+end_time_nj.getSeconds());
		$("#nj-diff-time").val(time_diff_nj+" msecs");
 		$('#nodejs_data_table > tr').remove();
 		var html = '';
 		for(var i = 1; i < dat.length; i++)
 			html += '<tr><td>' + dat[i] + '</td></tr>';

 		$('#nodejs_data_table').append(html);
 	}
	};
	 
	//open websocket callback
	 wsnj.onopen = function (evt) {
	};
	
	$(".get-last-sql").click(function () {
		wsnj.send("Get SQL").val();	
 
	});
	
	$(".change-unit").click(function () {	
		
		if(curr_unit == 0){
			curr_unit = 1;
			var con_temp = parseFloat($("#output-vals-temp-nj").val());
			con_temp = (con_temp * (9/5) + 32).toFixed(2);
			$("#output-vals-temp-nj").val(con_temp + " F");
		}
		else{
			curr_unit = 0;
			var con_temp = parseFloat($("#output-vals-temp-nj").val());
			con_temp = ((con_temp - 32) * (5/9)).toFixed(2);
			$("#output-vals-temp-nj").val(con_temp + " C");
		}

	});
	
	$(".compare-datasets").click(function() {
		start_time_nj = new Date($.now());
		$("#nj-start-time").val(start_time_nj.getHours()+":"+start_time_nj.getMinutes()+":"+start_time_nj.getSeconds());
		wsnj.send("Get Last NJS Ten Values").val();
	});
	
	
	//Close websocket callback
 	 wsnj.onclose = function (evt) {
		 
 	 	$("#output-vals-time-nj").val("");
 	 	$("#output-vals-temp-nj").val('');
 	 	$("#output-vals-humi-nj").val('');
 	 	$("#nj-end-time").val('');
		$("#nj-diff-time").val('');
		$("#nj-start-time").val('');
		$('#nodejs_data_table > tr').remove();
 	 }; 	 
 	 

});

