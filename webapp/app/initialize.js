window.$ = require('jquery')

document.addEventListener('DOMContentLoaded', function() {
  // do your setup here
  console.log('Initialized app');



  if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/static/sw.js').then(function(reg) {
        console.log('Successfully registered service worker', reg);
    }).catch(function(err) {
        console.warn('Error whilst registering service worker', err);
    });
  }


		window.addEventListener('online', function(e) {
				// Resync data with server.
				console.log("You are online");
		}, false);

		window.addEventListener('offline', function(e) {
				// Queue up events for server.
				console.log("You are offline");
		}, false);


		// Check if the user is connected.
		if (navigator.onLine) {
				// do online stuff
				console.log("online");
		} else {
				// Show offline message
				console.log("offline");
		}

		url = new URL(window.location.href);
    roomName = url.searchParams.get("roomName") || ''
		$("#roomName").html(roomName);
		
});


// https://developer.mozilla.org/en-US/docs/Web/API/File/Using_files_from_web_applications#Accessing_selected_file(s)
window.uploadImage = function() {
		console.log("upload an image");
		$("#status").html("uploading");
		file = document.getElementById('cameraInput').files[0];

		
    var FR= new FileReader();
    
    FR.addEventListener("load", function(e) {
				// base64 encoded image

				// look up the room name if it exists ?roomname=blah else
				// just call the room default
				url = new URL(window.location.href);
				roomName = url.searchParams.get("roomName") || 'default'
				
				console.log(roomName);
				$.post("/upload", {imgdata: e.target.result, roomName: roomName }, function () {
						$("#status").html("Image uploaded");

						// after 2 seconds, clear the message out
						window.setTimeout( function() { $("#status").html(""); }, 6000);
				});
				
    }); 
    
    FR.readAsDataURL( file );
}
