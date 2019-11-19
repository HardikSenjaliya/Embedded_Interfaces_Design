$(document).ready(function(){
    
    //tornado globals
    var wst;
    var host = "localhost";
    var port = "8888";
    var uri = "/ws";
    var lockstat = 0;
    
    $(".project").hide();
    $("#lockimg").hide();
    $("#unlockimg").hide();
    
    $(".connect").click(function (){
        
        var un = $("#username").val();
        var pw = $("#password").val ();
        
        if(un == ' ' || pw == ' ')
            console.log("Fill in the values to login..");
        
        if(un == "admin" && pw == "1234"){
            // create websocket instance
            console.log("Connected to system");
            wst = new WebSocket("ws://" + host + ":" + port + uri);  //tornado
            $("#username").val('');
            $("#password").val('');
            $(".connect").hide();
        
            $(".login").hide();
            
            if(lockstat == 1)
                $("#unlockimg").show();
            else
                $("#lockimg").show();
        
            $(".project").show();
            
        }
        
        else{

            console.log("Fill in the correct credentials..");
            $("#username").val('');
            $("#password").val('');
        }
        
        // Handle incoming websocket message callback
        $(".force-lock-door").click(function (){
            
            console.log("Locked");
            $("#unlock-name").val('Force Lock');
            $("#unlockimg").hide();
            $("#lockimg").show();
            lockstat=0;
        });
                        
        $(".force-unlock-door").click(function (){
            
            console.log("Unlocked");
            $("#unlockimg").show();
            $("#unlock-name").val('Force Unlock');
            $("#lockimg").hide();
            lockstat=1;
        });
        
        
        $(".logout").click(function (){
            
            console.log("Logged Out");
            $("#username").val('');
            $("#password").val('');
            $("#add-remove-status").val('');


            $(".project").hide();
            $("#lockimg").hide();
            $("#unlockimg").hide();
            $(".login").show();
            $(".connect").show();

        });
            
            

        
     });
    
    
});
    
