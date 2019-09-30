const http = require('http');
const WebSocketServer = require('websocket').server;

const server = http.createServer();
server.listen(9898);

const wsServer = new WebSocketServer({
    httpServer: server
});

wsServer.on('request', function (request) {
    const connection = request.accept(null, request.origin);

    connection.on('message', function (message) {
            if (message.utf8Data == "Get SQL"){
                console.log('Received Message:', message.utf8Data);
                connection.sendUTF(20);
            }
   /*         else if (message.utf8Data == "Temperature-NJS"){
                console.log('Received Message:', message.utf8Data);
                connection.sendUTF(40+"C");
            }*/
            
    });
    connection.on('close', function (reasonCode, description) {
        console.log('Client has disconnected.');
    });
});



