from srv.optyspes.eleves import Eleves
from srv.optyspes.algo import Gen
import base64

def init():
    global ELEVES, TASK
    ELEVES = Eleves()
    TASK = Gen()

def stopServer(data):
    if len(data) > 0:
        raise ValueError("Too many argument")
    TASK.stop()
    return None, None, None

def upload(data):
    global ELEVES
    if len(data) == 0:
        ELEVES = Eleves()
    else:
        ELEVES = Eleves(base64.b64decode(data).decode('utf-8'))
    return ELEVES.getData(), 'json', None

def getData(data):
    global ELEVES
    if len(data) > 0:
        raise ValueError("Too many argument")
    return ELEVES.getData(), 'json', None

def getStatus(data):
    global ELEVES, TASK
    if len(data) > 0:
        raise ValueError("Too many argument")
    # TASK.ask(ELEVES)
    return ELEVES.getStatus(), 'json', None

def download(id):
    global ELEVES
    return ELEVES.getCSV(id), 'csv', {'Content-Disposition':f'attachment;filename="résultat_{int(id[3:])}.csv"'}

# def update(data):
#     return ELEVES.update(data), 'json'

def start(data):
    global TASK, ELEVES
    if len(data) > 0:
        raise ValueError("Too many argument")
    if ELEVES.isEmpty():
        return '{"status":"FAIL"}', 'json', None
    return TASK.add(ELEVES), 'json', None

def stop(data):
    global TASK
    if len(data) > 0:
        raise ValueError("Too many argument")
    return TASK.remove(ELEVES), 'json', None

SERVICE = {
    "/upload":upload,       # in: csv,  out: json
    "/download":download,   # in: id,   out: csv
    "/getdata":getData,     # in: none, out: json
    "/getstatus":getStatus, # in: none, out: json
    # "/update":update,       # in: json, out: json
    "/start":start,         # in: none, out: json
    "/stop":stop,           # in: none, out: json
    "/quit":stopServer,     # in: none, out: none
}