import random
import json
import math
from multiprocessing import Manager

class Eleves:

    def __init__(self, csv=''):
        self.matieres = {}
        self.config = {}
        self.result = Manager().list()
        self.resultTmp = Manager().dict()
        self.solution_trouve = False

        if csv:
            csv = csv.replace('\r\n', '\n')
            csv = csv.replace('\n\r', '\n')
            csv = csv.split('\n')
            noms_matieres = csv[0].replace('\n', '').split(';')[3:]
            nb_eleves_matieres = csv[1].replace('\n', '').split(';')[3:]

            for ligne in csv[2:]:
                option = ligne.replace('\n', '').split(';')
                noms = option[0]+";"+option[1]+";"+option[2]
                option = option[3:]
                spe = []
                for i in range(len(noms_matieres)):
                    if (option[i] != '') and (int(option[i]) == 1):
                        spe.append(i)
                self.matieres[noms] = spe

            for opt in range(len(noms_matieres)):
                # noms, nb classe, nb eleves/classe, nb eleves
                tmp , classe = self._getNbEleve(opt, int(nb_eleves_matieres[opt]))
                self.config[opt] = (noms_matieres[opt], classe, 0 if (classe == 0) else (tmp / classe), int(nb_eleves_matieres[opt]), tmp)
                print(noms_matieres[opt], ":", tmp, "soit", classe, "classe(s)")

    def _getNbEleve(self, opt, nb_eleve):
        nb = [m for _ , matiere in self.matieres.items() for m in matiere].count(opt)
        cl = 0
        if nb != 0:
            cl = math.ceil(nb/nb_eleve)
        return nb, cl

    def isEmpty(self):
        return len(self.config) == 0

    def getData(self):
        if len(self.config) == 0:
            default_data = '<div class="my-3 border rounded border-muted bg-light text-muted d-flex align-items-center flex-column justify-content-center font-weight-bold" style="height:calc(100vh - 32px);"><i class="fas fa-file-upload fa-9x"></i>Déposer un fichier CSV ici.</div>'
            return json.dumps(
            {
                'status':'OK',
                'innerHTML':{
                    'param':default_data,
                    'eleves':default_data,
                    'result':default_data
                }
            })

        e = '<table class="table table-striped my-3"><thead class="thead-dark"><th scope="col">Classe</th><th scope="col">Noms</th><th scope="col">Prénom</th>'
        for k in range(len(self.config)):
            n, _, _, _, _ = self.config[k]
            e += f'<th scope="col">{n}</th>'
        e += "</thead><tbody>"
        for k in self.matieres:
            n = k.split(';')
            e += f'<tr><td scope="row">{n[0]}</td><td>{n[1]}</td><td>{n[2]}</td>'
            t = [0]*len(self.config)
            for i in self.matieres[k]:
                t[i] = 1
            for i in t:
                e += f'<td class="text-center"><input type="checkbox" {"checked"*i} disabled></td>'
            e += "</tr>"
        e += "</tbody></table>"

        c = '<table class="table table-striped my-3"><thead class="thead-dark"><th scope="col">Spécialité</th><th scope="col">Nb élèves max/groups</th><th scope="col">Nb élèves</th><th scope="col">Nb groups</th></thead><tbody>'
        for k in range(len(self.config)):
            n, t, _, cl, nb = self.config[k]
            c += f'<tr><td scope="row">{n}</td><td>{cl}</td><td>{nb}</td><td>{t}</td></tr>'
        c += '</tbody></table>'

        r = {
                'status':'OK',
                'innerHTML':{
                    'param':c,
                    'eleves':e,
                    'result':self.__getResult(),
                }
            }

        if (self.solution_trouve):
            self.solution_trouve = False
            r['message'] = {'color':'success', 'text':'Une solution a été trouvé !'}

        return json.dumps(r)

    def tempResult(self, id, p, it):
        self.resultTmp[id] = (it, p)

    def addResult(self, id, p):
        self.result.append((len(self.result), p))
        del self.resultTmp[id]
        if p.score < 100:
            self.solution_trouve = True

    def getID(self):
        pos = 0
        for i in range(1000):
            if i not in self.resultTmp:
                self.resultTmp[i] = _Population(self)
                return i
        raise Exception("get id range error")

    def getPopulation(self, nb):
        population = []
        for _ in range(nb):
            p = _Population(self)
            p.matieres = {noms:random.sample(matiere, k=len(matiere)) for noms, matiere in self.matieres.items()}
            p.calculeScore()
            population.append(p)
        return population

    def getCSV(self, id):
        id = int(id[3:])
        return self.result[id][1].getCSV()

    def __getResult(self):
        if len(self.result) == 0 and len(self.resultTmp) == 0:
            return "<div class='arrow arrow-left'>Clicker sur \"Calculer\" pour lancer l'optimisation.</div>"
        m = ""
        tmp = []
        for p in self.result:
            tmp.append((p[1].score, p[1].getHTML(download=p[0])))
        for k in self.resultTmp.keys():
            tmp.append((self.resultTmp[k][1].score, self.resultTmp[k][1].getHTML(progress=self.resultTmp[k][0])))
        tmp.sort(key=lambda x: x[0], reverse=False)
        for i in tmp:
            m += i[1]
        return m

    def getStatus(self):
        r = {
                'status':'OK',
                'innerHTML':{
                    'result':self.__getResult(),
                }
            }

        if (self.solution_trouve):
            self.solution_trouve = False
            r['message'] = {'color':'success', 'text':'Une solution a été trouvé !'}

        return json.dumps(r)


class _Population:

    def __init__(self, eleves):
        self.eleves = eleves
        self.matieres = {}
        self.score = None
        self.html = ""

    def calculeScore(self):
        self.score = 0
        test_nb_classe = True
        for noms, tmp in self.eleves.config.items():
            _, objectif, moyenne, nb_eleve, _ = tmp
            elems = []
            nb_classe = 0
            for i in range(len(next(iter(self.matieres.values())))):
                elem, classe = self.getNbElevePos(noms, i, nb_eleve)
                nb_classe += classe
                if classe > 1:
                    elems += [moyenne for _ in range(classe-1)]
                    elems.append(elem - (moyenne * (classe-1)))
                else:
                    elems.append(elem)
            elems.sort(reverse=True)
            for i in range(objectif):
                self.score += math.floor(math.fabs(moyenne - elems[i]))
            for i in range(objectif, nb_classe):
                self.score += math.floor(elems[i]) * 100 * (nb_classe - objectif)
            test_nb_classe &= nb_classe == objectif
        if not test_nb_classe:
            self.score += 100

    def getNbElevePos(self, opt, pos, nb_eleve):
        nb = [matiere[pos] for _ , matiere in self.matieres.items()].count(opt)
        cl = 0
        if nb != 0:
            cl = math.ceil(nb/nb_eleve)
        return nb, cl

    def melanger(self, eleve, mutation):
        resultat = _Population(self.eleves)
        mat = {noms:random.choice([matiere, eleve.matieres[noms]]) for noms, matiere in self.matieres.items()}
        if random.random() < mutation:
            noms, matiere = random.choice(list(mat.items()))
            mat[noms] = random.sample(matiere, k=len(matiere))
        resultat.matieres = mat
        resultat.calculeScore()
        return resultat

    def getCSV(self):
        sortie = "CLASSE;NOM;PRENOM;"
        for i in range(len(next(iter(self.matieres.values())))):
            sortie += "Groupe %d;" %(i+1)
        sortie += "\n"
        for noms, matiere in self.matieres.items():
            sortie += noms
            for i in matiere:
                if i >= 0 :
                    sortie += ";" + self.eleves.config[i][0]
                else:
                    sortie += ";"
            sortie += ";\n"
        return sortie
    
    def getHTML(self, progress=-1, download=-1):
        if self.html == "":
            color = "success" if self.score < 100 else "danger"
            p = ""
            if progress > -1:
                p = f'<div class="progress"><div class="progress-bar progress-bar-striped progress-bar-animated bg-{color}" role="progressbar" style="width: {progress}%" aria-valuenow="{progress}" aria-valuemin="0" aria-valuemax="100"></div></div>'
            d = ""
            if download > -1:
                d = f'<div class="mt-3"><form action="/download" method="post"><input type="hidden" name="id" value="{download}"><button type="submit" class="btn btn-secondary"><i class="fas fa-download"></i> Télécharger</button></form></div>'
            m = f'<div class="border border-{color} rounded m-3">{p}<div class="row pr-4"><div class="col-2 text-center my-auto"><svg viewBox="0 0 140 140" style="height: 8rem;width: 8rem;" preserveAspectRatio="xMinYMin meet"><g><circle r="50%" cx="50%" cy="50%" class="c_{color}" /><text class="t_{int(math.log10(self.score + 0.1)) + 1}" x="50%" y="50%" text-anchor="middle" dy="0.3em">{self.score}</text></g></svg>{d}</div><table class="col-10 table table-striped mt-3"><tbody>'
            k=0
            for noms, tmp in self.eleves.config.items():
                if k == 0:
                    m+='<tr><td scope="row">'
                elif k % 2 == 0:
                    m+='</td></tr><tr><td scope="row">'
                else:
                    m+='</td><td>'
                k+=1
                m+=f'{self.eleves.config[noms][0]}</td><td>'
                _, objectif, _, nb_eleve, _ = tmp
                nb_classe = 0
                L = []
                for i in range(len(next(iter(self.matieres.values())))):
                    elem, classe = self.getNbElevePos(noms, i, nb_eleve)
                    nb_classe += classe
                    if classe == 0:
                        pass
                    elif classe == 1:
                        L.append(elem)
                    else: 
                        for _ in range(classe-1):
                           L.append(elem // classe)
                           elem -= elem // classe
                        L.append(elem)
                L.sort(reverse=True)
                color_c = "success" if nb_classe == objectif else "danger"
                for i in L:
                    s = int(math.log10(i + 0.1)) + 1
                    m+= f'<svg class="mr-1" viewBox="0 0 140 140" style="height: 2rem;width: 2rem;" preserveAspectRatio="xMinYMin meet"><g><circle r="50%" cx="50%" cy="50%" class="c_{color_c}" /><text class="t_{s}" x="50%" y="50%" text-anchor="middle" dy="0.3em">{i}</text></g></svg>'
            m+="</td></tr></tbody></table></div></div>"
            if progress == -1:
                return m
            else:
                self.html = m
        return self.html