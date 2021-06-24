
document.getElementById('inp').onchange = function(e) {
    var img = new Image();
    img.onload = draw;
    img.onerror = failed;
    img.src = URL.createObjectURL(this.files[0]);
  };



function draw() {
    var canvas = document.getElementById('canvas');
    canvas.width = this.width;
    canvas.height = this.height;
    var ctx = canvas.getContext('2d');
    //scale ratio 15%
    ctx.beginPath();
    ctx.rect(1000, 50, 400, 700);
    ctx.fillStyle = 'grey';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = 'black';
    ctx.stroke();
    
    ctx.drawImage(this, 935,0,547,820);
   
}

function failed() {
    console.error("The provided file couldn't be loaded as an Image media");
}

// function draw_image() {
//   var canvas = document.getElementById
//   ReadableStream.ReadableStream(imageFile);
//   ReadableStream.onloaded = function (e){
//     PaymentAddress
//   }
// }


/*
let imgInput = document.getElementById('imageInput');
  imgInput.addEventListener('change', function(e) {
    if(e.target.files) {
      let imageFile = e.target.files[0]; //here we get the image file
      var reader = new FileReader();
      reader.readAsDataURL(imageFile);
      reader.onloadend = function (e) {
        var myImage = new Image(); // Creates image object
        myImage.src = e.target.result; // Assigns converted image to image object
        myImage.onload = function(ev) {
          var myCanvas = document.getElementById("myCanvas"); // Creates a canvas object
          var myContext = myCanvas.getContext("2d"); // Creates a contect object
          myCanvas.width = myImage.width; // Assigns image's width to canvas
          myCanvas.height = myImage.height; // Assigns image's height to canvas
          myContext.drawImage(myImage,0,0); // Draws the image on canvas
          let imgData = myCanvas.toDataURL("image/jpeg",0.75); // Assigns image base64 string in jpeg format to a variable
        }
      }
    }
  });
  */