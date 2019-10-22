    $(document).ready(function(){
        
         $(".page_proj2").hide();    
        
        //tornado globals
        var wst;
        var host = "localhost";
        var port = "8888";
        var uri = "/ws";

        var curr_unit_t = 0;
        var curr_unit_nj = 0;
        var start_time_tornado = 0;
        var end_time_tornado = 0;
        var time_diff_tornado = 0;
        
        
        //nodejs globals
        var wsnj;
        var start_time_nj = 0;
        var end_time_nj = 0;
        var time_diff_nj = 0;

        // Project 3 Aws Things
      
      
        AWS.config.region = 'us-east-1'; // Region
        AWS.config.credentials = new AWS.CognitoIdentityCredentials({
            IdentityPoolId: 'us-east-1:42d90798-2435-42f2-a47a-bd346c8415a8',
        });
       
        AWS.config.update({region: 'us-east-1'});


        const sqs = new AWS.SQS({apiVersion: '2012-11-05'});
        const queueUrl = 'https://sqs.us-east-1.amazonaws.com/595492067297/mySQSQueue';
        var num_reading = 1;
        var available_messages = 0;

        const one_message_params = {
            QueueUrl: queueUrl,
            MaxNumberOfMessages:1,
            VisibilityTimeout:0,
            WaitTimeSeconds:0
        };
        

        const queue_attr_params = {
             QueueUrl: queueUrl, /* required */
                AttributeNames: [
                    "ApproximateNumberOfMessages"
                ]
        };
     
        function get_num_messages(){
            sqs.getQueueAttributes(queue_attr_params, function(err, data) {
                if (err) console.log(err, err.stack);
                else{
                    //message = data.Attributes;
                    console.log('Number of Messages', data.Attributes.ApproximateNumberOfMessages);
                    available_messages = data.Attributes.ApproximateNumberOfMessages;
                }     
            });    
        }

       var html = '';
       html += '<tr>';
       html += '<td>' + 'Sr' + '</td>';
       html += '<td>' + 'Temperature' + '</td>';
       html += '<td>' + 'Humidity' + '</td>';
       html += '</tr>';
       $('#sqs_data_table').append(html);

        function receiveMessagefromQ(){

            sqs.receiveMessage(one_message_params, (err, data) => {

                    if(err){
                        return;             
                    }

                if(!data.Messages){
                    console.log('No Messages');
                }

                const message = JSON.parse(data.Messages[0].Body);
                console.log('Message Received', message);
                console.log('Temperature: ', message.temperature);
                console.log('Humidity:', message.humidity);

                    if(num_reading < 21){
                    var html = '';
                    html += '<tr>';
                    html += '<td>' + num_reading + '</td>';
                    html += '<td>' + message.temperature + '</td>';
                    html += '<td>' + message.humidity + '</td>';
                    html += '</tr>';

                    $('#sqs_data_table').append(html);
                    num_reading += 1;
                }else{
                         $('#sqs_data_table > tr').remove();
                         num_reading = 1;
                         var html = '';
                    html += '<tr>';
                    html += '<td>' + 'Sr' + '</td>';
                    html += '<td>' + 'Temperature' + '</td>';
                    html += '<td>' + 'Humidity' + '</td>';
                    html += '</tr>';
                       $('#sqs_data_table').append(html);
                        var html = '';
                    html += '<tr>';
                    html += '<td>' + num_reading + '</td>';
                    html += '<td>' + message.temperature + '</td>';
                    html += '<td>' + message.humidity + '</td>';
                    html += '</tr>';

                    $('#sqs_data_table').append(html);
                        num_reading += 1;                        
                                                        
                }

                const delete_message_params = {
                            QueueUrl: queueUrl,
                            ReceiptHandle: data.Messages[0].ReceiptHandle
                };
                    
                sqs.deleteMessage(delete_message_params, (err, data) => {
                    if(err){
                        console.log(err, err.stack);                       
                    }else{
                        console.log('Successfully Deleted Message');                       
                    }
                });

            });
        }
        

        $(".single-sqs").click(function(){
            receiveMessagefromQ();
        });

        $(".all-sqs").click(function(){
            
            get_num_messages();
            for(i = 0; i < available_messages; i++){
                receiveMessagefromQ();
            }
            
            available_messages = 0;

        });


        $(".num-messages").click(function(){
            get_num_messages();
            console.log('Recevied Count', available_messages);
            $('#message-count').val(available_messages);
            available_messages = 0;
        });


        $(".log-in").click(function (){
         // create websocket instance
         wst = new WebSocket("ws://" + host + ":" + port + uri);  //tornado
         wsnj = new WebSocket('ws://' + host + ':9898/ws'); //nodejs
         
         //$(".page_proj2").show();
         $(".log-in").attr("disabled", true);

         // Handle incoming websocket message callback
         wst.onmessage = function(evt) {
            
            var rcvd_message = evt.data.split(',');

            if(rcvd_message[0] == "Get Current Sensor Values"){
                if(rcvd_message[1] == "Sensor Disconnected"){
                    $("#sensor_status").val(rcvd_message[1]);
                    $("#output-vals-time").val('');
                    $("#output-vals-temp").val('');
                    $("#output-vals-humi").val('');
                }else{
                    $("#sensor_status").val('');
                    $("#output-vals-time").val(rcvd_message[1]);
                    $("#output-vals-temp").val(rcvd_message[2]);
                    $("#output-vals-humi").val(rcvd_message[3] + "%");
                }
            }
            else if(rcvd_message[0] == "Get Last Ten Values"){
                $("#sensor_status").val(''); 
                end_time_tornado = new Date($.now());
                time_diff_tornado = end_time_tornado.getTime() - start_time_tornado.getTime();
                $("#tornado-end-time").val(end_time_tornado.getHours()+":"+end_time_tornado.getMinutes()+":"+end_time_tornado.getSeconds());
                $("#tornado-diff-time").val(time_diff_tornado+" msecs");
                $('#tornado_data_table > tr').remove();
                var html = '';
                for(var i = 1; i < rcvd_message.length; i++)
                    html += '<tr><td>' + rcvd_message[i] + '</td></tr>';

                $('#tornado_data_table').append(html);

            }else if(rcvd_message[0] == "Wait for 10 Readings"){
                $("#sensor_status").val('Wait...');    
            }else if(rcvd_message[0] == "Graph Available"){
                $("#sensor_status").val('')    
            }
           
         };
         
         
             
         wsnj.onmessage = function (evt) {
            
            var dat = evt.data.split(',');
                
            if(dat[0] == "Get SQL"){
                $("#output-vals-time-nj").val(dat[1]);
                $("#output-vals-temp-nj").val(dat[2]);
                $("#output-vals-humi-nj").val(dat[3] + " %");
            }

            else if(dat[0] == "Get Last Ten Values"){

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
         
         
         

         // Close Websocket callback for tornado
         wst.onclose = function(evt) {

            $("#output-vals-time").val("");
            $("#output-vals-temp").val('');
            $("#output-vals-humi").val('');
            $("#tornado-end-time").val('');
            $("#tornado-diff-time").val('');
            $("#tornado-start-time").val('');
            $('#temp-graph img').remove();
            $('#humi-graph img').remove();
            $('#tornado_data_table > tr').remove();
            $(".log-in").attr("disabled", false);
            //$(".page_proj2").hide();

         };
         
         
            
        //Close websocket callback for nodejs
         wsnj.onclose = function (evt) {
             
            $("#output-vals-time-nj").val("");
            $("#output-vals-temp-nj").val('');
            $("#output-vals-humi-nj").val('');
            $("#nj-end-time").val('');
            $("#nj-diff-time").val('');
            $("#nj-start-time").val('');
            $('#nodejs_data_table > tr').remove();
            $(".log-in").attr("disabled", false);
            //$(".page_proj2").hide();
         };      
         

         // Open Websocket callback for tornado
        wst.onopen = function(evt) { 
            console.log("Tornado socket open");
            
        };  
        
        //open websocket callback for nodejs
         wsnj.onopen = function (evt) {
             console.log("Nodejs socket open");
             
        };
    });

        $(".get-vals-tornado").click(function() {
            wst.send("Get Current Sensor Values");
        });
        
        $(".change-unit").click(function() {
        
            if($("#output-vals-temp").val() != ''){
                if(curr_unit_t == 0){
                    curr_unit_t = 1;
                    if($("#output-vals-temp").val() != ''){
                        var con_temp = parseFloat($("#output-vals-temp").val());
                        con_temp = (con_temp * (9/5) + 32).toFixed(2);
                        $("#output-vals-temp").val(con_temp + " F");
                    }
                }else{
                    curr_unit_t = 0;
                    if($("#output-vals-temp").val() != ''){
                        var con_temp = parseFloat($("#output-vals-temp").val());
                        con_temp = ((con_temp - 32) * (5/9)).toFixed(2);
                        $("#output-vals-temp").val(con_temp + " C");
                    }
                }
            }
            
            if($("#output-vals-temp-nj").val() != ''){
                if(curr_unit_nj == 0){
                    curr_unit_nj = 1;
                    if($("#output-vals-temp-nj").val() != ''){
                        var con_temp = parseFloat($("#output-vals-temp-nj").val());
                        con_temp = (con_temp * (9/5) + 32).toFixed(2);
                        $("#output-vals-temp-nj").val(con_temp + " F");
                    }
                }else{
                    curr_unit_nj = 0;        
                        if($("#output-vals-temp-nj").val() != ''){
                        var con_temp = parseFloat($("#output-vals-temp-nj").val());
                        con_temp = ((con_temp - 32) * (5/9)).toFixed(2);
                        $("#output-vals-temp-nj").val(con_temp + " C");
                    }
                }
            }

        });
        

        $(".compare-datasets").click(function() {
            
            start_time_nj = new Date($.now());
            $("#nj-start-time").val(start_time_nj.getHours()+":"+start_time_nj.getMinutes()+":"+start_time_nj.getSeconds());
            
            start_time_tornado = new Date($.now());
            $("#tornado-start-time").val(start_time_tornado.getHours()+":"+start_time_tornado.getMinutes()+":"+start_time_tornado.getSeconds());
           
                   
            console.log("nodejs");
            //nodejs query
            wsnj.send("Get Last Ten Values");
            
            console.log("tornado");
            //tornado query
            wst.send("Get Last Ten Values");
            
            
        });

        $(".get-temp-graph").click(function(){
            wst.send("Get Temp Graph");
            $('#temp-graph img').remove();
            $('#temp-graph').append('<img src="http://localhost:8888/tempplot.png?id=performance.now()" alt="temp-graph" style="width:400px;height:400px;border-radius:10px;"/>');
        });

        $(".get-humi-graph").click(function(){
            wst.send("Get Humi Graph");
            $('#temp-graph img').remove();
            $('#temp-graph').prepend('<img src="http://localhost:8888/humidityplot.png?id=Math.random()" alt="humi-graph" style="width:400px;height:400px;border-radius:10px;"/>');
        });
        
        
        $(".get-last-sql").click(function () {
            wsnj.send("Get SQL");   
        });
        
        

        /*clear all data in all fields*/
        $(".clear-data").click(function() {
            
            $("#output-vals-time").val('');
            $("#output-vals-temp").val('');
            $("#output-vals-humi").val('');
            $("#tornado-end-time").val('');
            $("#tornado-diff-time").val('');
            $("#tornado-start-time").val('');
            $('#temp-graph img').remove();
            $('#humi-graph img').remove();
            $('#tornado_data_table > tr').remove();
            
            $("#output-vals-time-nj").val('');
            $("#output-vals-temp-nj").val('');
            $("#output-vals-humi-nj").val('');
            $("#nj-end-time").val('');
            $("#nj-diff-time").val('');
            $("#nj-start-time").val('');
            $('#nodejs_data_table > tr').remove();
            
            $(".log-in").attr("disabled", true);
        });

        $(window).bind('beforeunload',function(){

            $("#output-vals-time").val('');
            $("#output-vals-temp").val('');
            $("#output-vals-humi").val('');
            $("#tornado-end-time").val('');
            $("#tornado-diff-time").val('');
            $("#tornado-start-time").val('');
            $('#temp-graph img').remove();
            $('#humi-graph img').remove();
            $('#tornado_data_table > tr').remove();
            
            $("#output-vals-time-nj").val('');
            $("#output-vals-temp-nj").val('');
            $("#output-vals-humi-nj").val('');
            $("#nj-end-time").val('');
            $("#nj-diff-time").val('');
            $("#nj-start-time").val('');
            $('#nodejs_data_table > tr').remove();
            
            $(".log-in").attr("disabled", true);
            
        });

    });
