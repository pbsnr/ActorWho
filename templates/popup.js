
let changeColor = document.getElementById('takePhoto');

changeColor.onclick = function startCapture(){
	h = 563; 
	w = 1000;
	console.log(h, w)
	navigator.mediaDevices.getDisplayMedia({ video: {width: w, height: h}, frameRate: { max: 1 }}).then((stream) => {
	   let track = stream.getVideoTracks()[0];
	   console.log(track)
	   let capture = new ImageCapture(track);
	   console.log(capture)	
	   return capture.grabFrame();
	}).then((bitmap) => {
	   //let canvas = document.createElement('canvas');
	   let canvas = document.getElementById("myCanvas");
	   //canvas.width = 3000
	   //canvas.height = 3000
	   let context = canvas.getContext('2d');
	   context.drawImage(bitmap, 0, 0, w, h)
	   return canvas.toDataURL();
	}).then((src) => {
	   // do something with the source
	   //console.log(src)
	   let data = JSON.stringify({img:src, title:"matrix"});
	   console.log("ok")
	   var xmlHttp = new XMLHttpRequest();
    	xmlHttp.open( "POST", "http://127.0.0.1:4000/upload", false ); // false for synchronous request
    	xmlHttp.send( data );
	}).catch(console.error)

}