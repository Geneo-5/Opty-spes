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
                self.config[opt] = (noms_matieres[opt], classe, 0 if (classe == 0) else (tmp / classe), int(nb_eleves_matieres[opt]))
                print(noms_matieres[opt], ":", tmp, "soit", classe, "classe(s)")

    def _getNbEleve(self, opt, nb_eleve):
        nb = [m for _ , matiere in self.matieres.items() for m in matiere].count(opt)
        cl = 0
        if nb != 0:
            cl = math.ceil(nb/nb_eleve)
        return nb, cl

    def getData(self):
        e = "<thead><th><div>Classe</div></th><th><div>Noms</div></th><th><div>Prénom</div></th>"
        for k in range(len(self.config)):
            n, _, _, _ = self.config[k]
            e += f'<th class="rotate"><div><span>{n}</span></div></th>'
        e += "</thead><tbody>"
        for k in self.matieres:
            n = k.split(';')
            e += f"<tr><td class='tc'>{n[0]}</td><td>{n[1]}</td><td>{n[2]}</td>"
            t = [0]*len(self.config)
            for i in self.matieres[k]:
                t[i] = 1
            for i in t:
                e += f'<td class="tc"><input type="checkbox" {"checked"*i} disabled></td>'
            e += "</tr>"
        e += "</tbody>"

        c = "<thead><th>Spécialité</th><th>Nombre d'élèves maximun par classe</th><th>Nombre de classes</th></thead><tbody>"
        for k in range(len(self.config)):
            n, t, _, cl = self.config[k]
            c += f"<tr><td>{n}</td><td class='tc'>{cl}</td><td class='tc'>{t}</td></tr>"
        c += "</tbody>"
        return json.dumps(
            {
                'status':'OK',
                'innerHTML':{
                    'spe':c,
                    'eleve':e,
                }
            })

    def tempResult(self, id, p, it):
        self.resultTmp[id] = (it, p)

    def addResult(self, id, p):
        self.result.append((len(self.result), p))
        del self.resultTmp[id]

    def getPopulation(self, nb):
        pos = 0
        for i in range(1000):
            if i not in self.resultTmp:
                self.resultTmp[i] = _Population(self)
                pos = i
                break
        population = []
        for _ in range(nb):
            p = _Population(self)
            p.matieres = {noms:random.sample(matiere, k=len(matiere)) for noms, matiere in self.matieres.items()}
            p.calculeScore()
            population.append(p)
        return pos, population

    def getCSV(self, id):
        id = int(id[3:])
        return self.result[id][1].getCSV()

    def getStatus(self):
        m = "<thead><th>#ID</th><th>Score</th><th>index</th></thead><tbody>"
        sortedResult = sorted(self.result, key=lambda x: x[1].score, reverse=False)
        i = 1
        tmp = []
        for p in sortedResult:
            color = "#80FF80" if p[1].score <= 100 else "#FF8080"
            tmp.append((p[1].score, f"<tr style='background-color:{color};'><td>{i}</td><td>{p[1].score}</td><td><form action='/download' method='post'><input type='hidden' name='id' value='{p[0]}'><button>Télécharger</button></form></td></tr>"))
            i += 1
        for k in self.resultTmp.keys():
            color = "#80FF80" if self.resultTmp[k][1].score <= 100 else "#FF8080"
            tmp.append((self.resultTmp[k][1].score, f"<tr style='background-color:{color};'><td></td><td>{self.resultTmp[k][1].score}</td><td><progress max='100' value='{self.resultTmp[k][0]}'>{self.resultTmp[k][0]}%</progress></td></tr>"))
        tmp.sort(key=lambda x: x[0], reverse=False)
        for i in tmp:
            m += i[1]
        m += "</tbody>"
        return json.dumps(
            {
                'status':'OK',
                'innerHTML':{
                    'resultat':m,
                }
            })

class _Population:

    def __init__(self, eleves):
        self.eleves = eleves
        self.matieres = {}
        self.score = None

    def calculeScore(self):
        self.score = 0
        test_nb_classe = True
        for noms, tmp in self.eleves.config.items():
            _, objectif, moyenne, nb_eleve = tmp
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