from optyspes.eleves import Eleves
from optyspes.algo import Gen

ELEVES = Eleves()
TASK = Gen()

def stopServer(data):
    if len(data) > 0:
        raise ValueError("Too many argument")
    raise KeyboardInterrupt

def upload(data):
    if len(data) == 0:
        ELEVES = Eleves()
    else:
        ELEVES = Eleves(data.decode('utf-8'))
    return ELEVES.getData()

def getData(data):
    if len(data) > 0:
        raise ValueError("Too many argument")
    return ELEVES.getData() 

def getStatus(data):
    if len(data) > 0:
        raise ValueError("Too many argument")
    TASK.ask(ELEVES)
    return ELEVES.getStatus() 

def download(id):
    return ELEVES.getCSV(id)

def update(data):
    return ELEVES.update(data)

def start(data):
    if len(data) > 0:
        raise ValueError("Too many argument")
    return TASK.add(ELEVES)

def stop(data):
    if len(data) > 0:
        raise ValueError("Too many argument")
    return TASK.remove(ELEVES)

SERVICE = {
    "/upload":upload,       # in: csv,  out: json
    "/download":download,   # in: id,   out: csv
    "/getdata":getData,     # in: none, out: json
    "/getstatus":getStatus, # in: none, out: json
    "/update":update,       # in: json, out: json
    "/start":start,         # in: none, out: json
    "/stop":stop,           # in: none, out: json
    "/quit":stopServer,     # in: none, out: none
}