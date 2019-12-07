$(document).ready(function(){
    
    //tornado globals
    var wst;
    var host = "localhost";
    var port = "8889";
    var uri = "/ws";
    var lockstat = 2;
    var wait =1;


	    
    $(".project").hide();
    $("#lockimg").hide();
    $("#unlockimg").hide();
    
   
   
    const bucket_name = 'eid-image-rekognition'
    
    define(function (require) {
	 const AWS = require ('aws-sdk');
	 
    }); 
	
	
	
    function AnonLog() {
    
    //Initialize the Amazon Cognito credentials provider
	AWS.config.region = 'us-east-1'; // Region
	AWS.config.credentials = new AWS.CognitoIdentityCredentials({
	IdentityPoolId: 'us-east-1:396a93f3-98af-4c19-ba4a-ca11dff8f653',	
	});
    
    // Make the call to obtain credentials
    AWS.config.credentials.get(function () {
      // Credentials will be available when this function is called.
      var accessKeyId = AWS.config.credentials.accessKeyId;
      var secretAccessKey = AWS.config.credentials.secretAccessKey;
      var sessionToken = AWS.config.credentials.sessionToken;
    });
  }	
	
    AnonLog();   
		
    AWS.config.update({region: 'us-east-1'});
       
    // Create S3 service object
    var s3 = new AWS.S3({
	apiVersion: "2006-03-01",
	params: { Bucket: bucket_name }
    });
				


    function addPhoto(userName) {
    
      var files = document.getElementById("userPhoto").files;
      if (!files.length) {
	return alert("Please choose a file to upload first.");
      }
    
      var file = files[0];
      var fileName = file.name;
    
	const params = {
		Bucket: bucket_name,
		Key: userName + '.jpg', // File name you want to save as in S3
		Body: file
    };

    // Uploading files to the bucket
    s3.upload(params, function(err, data) {
	if (err) {
	    throw err;
	}
	console.log(`File uploaded successfully. ${data.Location}`);
    $("#add-remove-status1").val('File added');
    });

    }
    
    
    
    function removePhoto(userName) {
	
	const params = {
		Bucket: bucket_name,
		Key: userName + '.jpg', // File name you want to save as in S3
		
	};

	
	//Deleting photo from S3
	s3.deleteObject(params, function(err, data) {
	    if (err) {
		throw err;
	    }
	    console.log(`File deleted successfully`);
        $("#add-remove-status2").val('File deleted');
    });

	
    }
   

    
    $(".connect").click(function (){
        

	var un = $("#username").val();
	var pw = $("#password").val ();
	
	if(un == ' ' || pw == ' ')
	    console.log("Fill in the values to login..");
	
	if(un == "admin" && pw == "1234"){
        
        
       // create websocket instance
        wst = new WebSocket("ws://" + host + ":" + port + uri);  //tornado
            	    
	    console.log("Login successful");
	    $("#username").val('');
	    $("#password").val('');
	    $(".connect").hide();
	
	    $(".login").hide();
        $("#unlockimg").hide();
		$("#lockimg").show();
        
		
	
	    $(".project").show();

	    
	}
	
	else{

	    console.log("Fill in the correct credentials..");
	    $("#username").val('');
	    $("#password").val('');
	}
    
    
     wst.onmessage = function(evt) {

         
        var rcvd_message = evt.data;
         
        if(lockstat == 0)
        {
            $("#unlock-name").val('Force Lock');
        }
        
        else if(lockstat == 1)
        {
            $("#unlock-name").val('Force Unlock');
        }
         
        else if(rcvd_message == "Lock" && lockstat != 1){
                
            console.log("Locked");
            $("#unlock-name").val(" ");
            $("#unlockimg").hide();
            $("#lockimg").show();
            
            
        }
        else if(rcvd_message == "Get Database"){
            //print
            console.log("Fetching database...");
        }
        else{
            if(lockstat !=0){
        
                console.log("Unlocked");
                $("#unlockimg").show();
                $("#unlock-name").val(rcvd_message);
                $("#lockimg").hide();
                
            }
        }
         
    };
        
    });
    
	$(".get-database").click(function (){
	    
	    console.log("Displaying database");
	    wst.send("Get Database");
	});    

       
	
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
	
	
	$(".add-user").click(function () {
	    console.log("Add User");
	    window.location.href = 'adduser.html';
	     
	});
	
	$(".submit1").click(function () {

	    var userName = $("#userName").val();
        addPhoto(userName);	
        

	}); 
    
    $(".submit2").click(function () {
	
	    var userName = $("#userName").val();

		removePhoto(userName);
	}); 
	
	$(".remove-user").click(function () {

	    console.log("Remove User");
	    window.location.href = 'removeuser.html';

	});
	
	
	$(".homePage").click(function () {

	    window.location.href = 'EIDClient.html';
    
	    		
	}); 	
    
});
    
