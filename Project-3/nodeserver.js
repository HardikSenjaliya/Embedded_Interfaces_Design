
const http = require('http');
const WebSocketServer = require('websocket').server;

const server = http.createServer();
server.listen(9898);

const wsServer = new WebSocketServer({
    httpServer: server
});

console.log("***  NodeJS websocket ***");

wsServer.on('request', function (request) {
    const connection = request.accept(null, request.origin);
     console.log("** Client has connected (NODEJS <--> Client) **");

    connection.on('message', function (message) {
        
        var mysql = require('mysql');
        
        var con = mysql.createConnection({
            host: "localhost",
            user: "hardyk",
            password: "mysql123",
            database: "EID_projectDB"
        });

        con.connect(function(err) {
            if (err) throw err;
        

            if (message.utf8Data == "Get SQL"){
               //console.log(message.utf8Data);

                var queryString = "SELECT * FROM sensor_values order by formatted_time desc limit 1";

                con.query(queryString, function(err, result, fields) {
                if (err) throw err;

                connection.sendUTF(message.utf8Data + "," + result[0].formatted_time+","+result[0].tempc+ " C" + "," +result[0].humidity);

             });
            }
         
            else if (message.utf8Data == "Get Last Ten Values"){
               
                console.log("Fetching last 10 values from NJS");
                var queryString1 = "SELECT * FROM sensor_values order by formatted_time desc limit 10";
                con.query(queryString1, function(err, result, fields) {
                if (err) throw err;
                
              //  console.log(result);
                  
                 connection.sendUTF(message.utf8Data +"," + result[0].humidity+"," +result[1].humidity+"," +result[2].humidity+"," +result[3].humidity+"," +result[4].humidity+"," +result[5].humidity+"," +result[6].humidity+"," +result[7].humidity+"," +result[8].humidity+"," +result[9].humidity);
                 
             });
            
            }
        
        });
        
            
    });
    connection.on('close', function (reasonCode, description) {
        console.log('Client has disconnected (NODEJS <--> Client)');
    });
    
    
});



