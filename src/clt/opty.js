function costum_allert(color, message) {
    document.getElementById('message').innerHTML = '<div class="mt-3 alert alert-'+ color +' alert-dismissible fade show" role="alert">' + message +'<button type="button" class="close" data-dismiss="alert" aria-label="Close"><span aria-hidden="true">&times;</span></button></div>'
}

function uploadFile(e) {
    if(e.dataTransfer.files){
        if(e.dataTransfer.files.length) {
            e.preventDefault();
            e.stopPropagation();
            var f = e.dataTransfer.files[0];
            if (!f.type.match('.csv')) {
                    costum_allert('danger', 'Le fichier doit être un <strong>CSV</strong> !')
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
        if (json.hasOwnProperty('message')) {
            costum_allert(json.message.color, json.message.text)
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
            s.checked = true;
            s.onclick = () => {
                s.checked = true;
                var xhttp = new XMLHttpRequest();
                xhttp.onreadystatechange = () => {
                    if (this.readyState == 4 && this.status == 200) {
                        var json = JSON.parse(this.responseText);
                        if (json.status == "OK") {
                            s.checked = false;
                            s.onclick = start;
                            clearInterval(id);
                            getStatus();
                        }
                    }
                };
                xhttp.open("POST", "stop", true);
                xhttp.setRequestHeader("Content-type", "application/json");
                xhttp.send('');
            }
        } else {
            document.getElementById("stop").checked = false;
        }
    }
}

function start(){
    document.getElementById("stop").checked = false;
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