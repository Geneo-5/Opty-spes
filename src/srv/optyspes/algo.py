import multiprocessing
from multiprocessing import Process, JoinableQueue, Manager, Lock
import time
import random
import os

# TODO migre to spawn instead
multiprocessing.set_start_method("fork")

NB_PROCESS = os.cpu_count()

NB_POPULATION = 100
NB_GENERATION = 256 * 30
PROBA_MUTATION = 0.01
PROBA_GARDER = 0.1
PROBA_SAUVER = 0.1

NB_GARDER = int(NB_POPULATION * PROBA_GARDER)
NB_SAUVER = int(NB_POPULATION * PROBA_SAUVER)

STATUS_OK = '{"status":"OK"}'
STATUS_FAIL = '{"status":"FAIL"}'

class Gen:

    def __init__(self):
        self.request = Manager().list()
        self.task = JoinableQueue(NB_PROCESS)
        self.proc = []
        self.lock_id = Lock()
        p = Process(target=self.run, args=(self.request, self.task, ))
        p.start()
        self.proc.append(p)
        for _ in range(NB_PROCESS):
            p = Process(target=self.evaluation, args=(self.request, self.task, ))
            p.start()
            self.proc.append(p)

    def stop(self):
        for p in self.proc:
            p.terminate()
            p.join()


    def evaluation(self, r, q):
        print("start evaluation")
        try:
            while True:
                task = q.get()
                with self.lock_id:
                    id = task.getID()
                p = task.getPopulation(NB_POPULATION)
                print(id, len(p[0].matieres))
                print("start gen", id)
                i = 0
                resultat_ok = False
                pas = 1
                while i < NB_GENERATION:
                    if len(r) == 0:
                        break
                    p.sort(key=lambda x: x.score, reverse=False)
                    
                    # test si on a une solution
                    if not resultat_ok and (p[0].score < 100):
                        resultat_ok = True
                        # on fait encore quelque tour
                        pas = max(1, (NB_GENERATION - i) / 10)

                    task.tempResult(id, p[0], min(100,(i * 100)//NB_GENERATION))
                    pg = p[:NB_GARDER]
                    pg += random.sample(p[NB_GARDER:], NB_SAUVER)
                    p = pg + [random.choice(pg).melanger(random.choice(pg), PROBA_MUTATION) for _ in range(len(pg), NB_POPULATION)]
                    i += pas

                task.addResult(id, p[0])
                q.task_done()
        except KeyboardInterrupt:
            pass

    def run(self, request, task):
        try:
            while True:
                if len(request) == 0:
                    time.sleep(3)
                    continue
                for _ in range(NB_PROCESS):
                    task.put(random.choice(request))
                task.join()
        except KeyboardInterrupt:
            pass
    #     print("Start runner")
    #     sleep = False
    #     while True:
    #         if sleep:
    #             print("sleep")
    #             time.sleep(10)
    #         sleep = False
    #         # with self.lock:
    #         if len(task) == 0:
    #             sleep = True
    #             continue
    #         else:
    #             print("task", len(taskTime))
    #             taskTime = { k: taskTime[k] for k in taskTime.keys() if time.time() - taskTime[k] < MAX_TIME }
    #             poolTask = []
    #             print("task filter", len(self.taskTime))
    #             while len(poolTask) < NB_PROCESS and len(task) != 0:
    #                 t = task.pop(0)
    #                 if t in taskTime:
    #                     poolTask.append(t)
    #                     task.append(t)
    #             if len(poolTask) == 0:
    #                 sleep = True
    #                 continue
    #         print("run pool", len(poolTask))
    #         with Pool(processes=NB_PROCESS) as pool:
    #             result = [pool.apply_async(evaluation,(t,)) for t in poolTask]
    #         print("wait pool", len(result))
    #         for r in result:
    #             r.get()

    def add(self, task):
        if task not in self.request:
            self.request.append(task)
            return STATUS_OK
        else:
            return STATUS_FAIL

    def remove(self, task):
        self.request[:] = []
        return STATUS_OK

    # def ask(self, task):
    #     # if task in self.taskTime:
    #     #     self.taskTime[task] = time.time()
    #     self.task.put(task)
    #     return STATUS_OK

