$(document).ready(function(){
    
    //tornado globals
    var wst;
    var host = "localhost";
    var port = "8888";
    var uri = "/ws";
    
    $(".project").hide();
    $(".unlocked").hide();
    
    $(".connect").click(function (){
        
        var un = $("#username").val();
        var pw = $("#password").val ();
        
        if(un == ' ' || pw == ' ')
            console.log("Fill in the values to login..");
        
        if(un == "admin" && pw == "1234"){
            // create websocket instance
            console.log("Connected to system");
            wst = new WebSocket("ws://" + host + ":" + port + uri);  //tornado
            $(".connect").hide();
        
            $(".login").hide();
        
            $(".project").show();
            
        }
        
        else{

            console.log("Fill in the correct credentials..");
            $("#username").val(' ');
            $("#password").val(' ');
        }
        
        // Handle incoming websocket message callback
        $(".force-lock-door").click(function (){
            
            console.log("Locked");
            $("#unlock-name").val('Force Lock');
            $(".unlocked").hide();
            $("#lockimg").show();
        });
                        
        $(".force-unlock-door").click(function (){
            
            console.log("Unlocked");
            $(".unlocked").show();
            $("#unlock-name").val('Force Unlock');
            $("#lockimg").hide();
        });
            

        
     });
    
    
});
    
