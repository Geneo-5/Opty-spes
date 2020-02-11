function uploadFile(e) {
    if(e.dataTransfer.files){
        if(e.dataTransfer.files.length) {
            e.preventDefault();
            e.stopPropagation();
            var f = e.dataTransfer.files[0];
            if (!f.type.match('.csv')) {
                    alert('Le fichier doit être un CSV');
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

function result() {
    getStatus()
    openDiv("result");
}

function started(){
    if (this.readyState == 4 && this.status == 200) {
        var json = JSON.parse(this.responseText);
        if (json.status == "OK") {
            result()
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

function openDiv(div) {
    document.getElementById(div).style.visibility = "visible";
}

function closeDiv(div) {
    document.getElementById(div).style.visibility = "hidden";
}

function volet() {
    var f = document.getElementById("f")
    var o = document.getElementById("o")
    if (f.style.display == "none") {
        o.style.display = "none"
        f.style.display = "block"
    } else {
        o.style.display = "block"
        f.style.display = "none"
    }
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