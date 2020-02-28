function uploadFile(e) {
    if(e.dataTransfer.files){
        if(e.dataTransfer.files.length) {
            e.preventDefault();
            e.stopPropagation();
            var f = e.dataTransfer.files[0];
            if (!f.type.match('.csv')) {
                    document.getElementById('message').innerHTML = '<div class="mt-3 alert alert-danger alert-dismissible fade show" role="alert">Le fichier doit être un <strong>CSV</strong> !<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
                    return false ;
            }
            var reader = new FileReader();
            reader.onload = handleReaderLoad;
            reader.readAsDataURL(f);   
        }  
    }
    return false;
}

function parseServerReturn(){
    if (this.readyState == 4 && this.status == 200) {
        var json = JSON.parse(this.responseText);
        if (json.status == "OK") {
            for (var i in json.innerHTML) {
                document.getElementById(i).innerHTML = json.innerHTML[i];
            }
        }
    }
}

function getStatus() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = parseServerReturn;
    xhttp.open("POST", "getstatus", true);
    xhttp.send();
}

function started(){
    if (this.readyState == 4 && this.status == 200) {
        var json = JSON.parse(this.responseText);
        if (json.status == "OK") {
            getStatus()
            var id = setInterval(getStatus, 3000);
            var s = document.getElementById("stop")
            s.innerText = "Arrêter le calculs"
            s.onclick = () => {
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = () => {
                    if (this.readyState == 4 && this.status == 200) {
                        var json = JSON.parse(this.responseText);
                        if (json.status == "OK") {
                            s.innerText = "Lancer le calcul"
                            clearInterval(id);
                        }
                    }
                };
                xhttp.open("POST", "stop", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send('');
            }
        }
    }
}

function start(){
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = started;
    xhttp.open("POST", "start", true);
    xhttp.send();
}

function handleReaderLoad(evt) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = parseServerReturn;
    xhttp.open("POST", "upload", true);
    xhttp.setRequestHeader("Content-type", "text/csv");
    xhttp.send(evt.target.result.split(',')[1]);
}

function preventDefault(event) {
    event.preventDefault();
}

function quit() {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = () => {
            close();
    };
    xhttp.open("POST", "quit", true);
    xhttp.send();
}

document.addEventListener("dragstart", preventDefault, false);
document.addEventListener("dragenter", preventDefault, false);
document.addEventListener("dragleave", preventDefault, false);
document.addEventListener("drag", preventDefault, false);
document.addEventListener("dragend", preventDefault, false);
document.addEventListener("dragover", preventDefault, false);
document.addEventListener("drop", preventDefault, false);
document.addEventListener("drop", uploadFile, false);

// Java script chargé, on récupère la dernière session.
var xhttp = new XMLHttpRequest();
xhttp.onreadystatechange = parseServerReturn;
xhttp.open("POST", "getdata", true);
xhttp.send();