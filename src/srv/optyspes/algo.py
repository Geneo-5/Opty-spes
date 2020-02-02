from multiprocessing import Pool
import time
from queue import Queue, Empty
from threading import Thread, Lock
import threading
import random
import os

NB_PROCESS = os.cpu_count()

NB_POPULATION = 100
NB_GENERATION = 256 * 30
PROBA_MUTATION = 0.01
PROBA_GARDER = 0.1
PROBA_SAUVER = 0.1

NB_GARDER = int(NB_POPULATION * PROBA_GARDER)
NB_SAUVER = int(NB_POPULATION * PROBA_SAUVER)

MAX_TIME = 60

STATUS_OK = b'{"status":"OK"}'
STATUS_FAIL = b'{"status":"FAIL"}'

class Gen:

    def __init__(self):
        self.taskTime = {}
        self.task = Queue()
        self.lock = Lock()
        thread = Thread(target=self.run)
        # thread.daemon = True
        thread.start()

    def run(self):
        while True:
            with self.lock:
                if self.task.empty():
                    time.sleep(10)
                    continue
                else:
                    self.taskTime = { k: t for k, t in self.taskTime if time.time() - t < MAX_TIME }
                    poolTask = []
                    try:
                        while len(poolTask) < NB_PROCESS:
                            t = self.task.get_nowait()
                            if t in self.taskTime:
                                poolTask.append(t)
                                self.task.put(t)
                    except Empty:
                        if len(poolTask) == 0:
                            continue
            with Pool(processes=NB_PROCESS) as pool:
                result = [pool.apply_async(self.evaluation,(t,)) for t, _ in self.taskTime]
            for r in result:
                r.get()

    def add(self, task):
        with self.lock:
            if task not in self.taskTime:
                self.taskTime[task] = time.time()
                self.task.put(task)
                return STATUS_OK
            else:
                return STATUS_FAIL

    def remove(self, task):
        with self.lock:
            if task not in self.taskTime:
                return STATUS_FAIL
            else:
                del self.taskTime[task]
                return STATUS_OK

    def ask(self, task):
        with self.lock:
            if task in self.taskTime:
                self.taskTime[task] = time.time()

    def evaluation(self, task):
        p = task.getPopulation(NB_POPULATION)
        for _ in range(NB_GENERATION):
            p.sort(key=lambda x: x.score, reverse=False)
            pg = p[:NB_GARDER]
            pg += random.sample(p[NB_GARDER:], NB_SAUVER)
            p = pg + [random.choice(pg).melanger(random.choice(pg), PROBA_MUTATION) for _ in range(len(pg), NB_POPULATION)]
        task.addResult(p[0])
