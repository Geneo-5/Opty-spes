function uploadFile(e) {
    if(e.dataTransfer.files){
        if(e.dataTransfer.files.length) {
                    // Stop the propagation of the event
                    e.preventDefault();
                    e.stopPropagation();
                    // $(this).css('border', '3px dashed green');
                    // Main function to upload
                    var f = e.dataTransfer.files[0];
                    // Only process image files.
                    if (!f.type.match('.csv')) {
                            alert('Le fichier doit être un CSV');
                            return false ;
                    }
                    var reader = new FileReader();
        
                    // When the image is loaded,
                    // run handleReaderLoad function
                    reader.onload = handleReaderLoad;
        
                    // Read in the image file as a data URL.
                    reader.readAsDataURL(f);   
        }  
    }
    else {
            //$(this).css('border', '3px dashed #BBBBBB');
    }
    return false;
}

function handleReaderLoad(evt) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          alert(this.responseText);
        }
      };
    xhttp.open("POST", "upload", true);
    xhttp.setRequestHeader("Content-type", ".csv");
    xhttp.send(evt.target.result.split(',')[1]);
}

function preventDefault(event) {
    event.preventDefault();
}

function alertFiles(event) {
    alert(event.dataTransfer.files);
}
document.addEventListener("dragstart", preventDefault, false);
document.addEventListener("dragenter", preventDefault, false);
document.addEventListener("dragleave", preventDefault, false);
document.addEventListener("drag", preventDefault, false);
document.addEventListener("dragend", preventDefault, false);
document.addEventListener("dragover", preventDefault, false);
document.addEventListener("drop", preventDefault, false);
document.addEventListener("drop", uploadFile, false);