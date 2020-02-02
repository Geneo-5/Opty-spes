import random
import math
import sys

NB_POPULATION = 100
NB_GROUPES = 3
NB_GENERATION = 256
PROBA_MUTATION = 0.01
PROBA_GARDER = 0.1
PROBA_SAUVER = 0.1
FICHIER_CSV = 'exemple.csv'

NB_GARDER = int(NB_POPULATION * PROBA_GARDER)
NB_SAUVER = int(NB_POPULATION * PROBA_SAUVER)

class Eleve:
    CONFIG = {}

    def __init__(self):
        self.matieres = {}
        self.score = None

    def melanger(self, eleve):
        resultat = Eleve()
        mat = {noms:random.choice([matiere, eleve.matieres[noms]]) for noms, matiere in self.matieres.items()}
        if random.random() < PROBA_MUTATION:
            noms, matiere = random.choice(list(mat.items()))
            mat[noms] = random.sample(matiere, k=len(matiere))
        resultat.matieres = mat
        resultat.calculeScore()
        return resultat

    def getRandom(self):
        resultat = Eleve()
        resultat.matieres = {noms:random.sample(matiere, k=len(matiere)) for noms, matiere in self.matieres.items()}
        resultat.calculeScore()
        return resultat

    def affiche(self, noms_matieres):
        sortie = "CLASSE;NOM;PRENOM;"
        for i in range(NB_GROUPES):
            sortie += "Groupe %d;" %(i+1)
        sortie += "\n"
        for noms, matiere in self.matieres.items():
            sortie += noms
            for i in matiere:
                if i >= 0 :
                    sortie += ";" + noms_matieres[i]
                else:
                    sortie += ";"
            sortie += ";\n"
        return sortie

    def stat(self):
        sortie = ""
        effectif = ""
        for noms, tmp in Eleve.CONFIG.items():
            objectif, _, nb_eleve = tmp
            nb_classe = 0
            effectif_out = "" 
            for i in range(NB_GROUPES):
                elem, classe = self.getNbElevePos(noms, i, nb_eleve)
                nb_classe += classe
                if elem == 0:
                    effectif_out += "  ,"
                else:
                     effectif_out += "%2d," %elem
            sortie += str(nb_classe) + "/" + str(objectif) + "|"
            effectif += "(" + effectif_out[:-1] + ")"
        return sortie[:-1] + effectif


    def calculeScore(self):
        self.score = 0
        test_nb_classe = True
        for noms, tmp in Eleve.CONFIG.items():
            objectif, moyenne, nb_eleve = tmp
            elems = []
            nb_classe = 0
            for i in range(NB_GROUPES):
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

    def getNbEleve(self, opt, nb_eleve):
        nb = [m for _ , matiere in self.matieres.items() for m in matiere].count(opt)
        cl = 0
        if nb != 0:
            cl = math.ceil(nb/nb_eleve)
        return nb, cl

def evaluation_eleves(eleves):
    for _ in range(NB_GENERATION):
        eleves_garder = eleves[:NB_GARDER]
        eleves_garder += random.sample(eleves[NB_GARDER:], NB_SAUVER)  
        nouveau_eleve = [random.choice(eleves_garder).melanger(random.choice(eleves_garder)) for _ in range(len(eleves_garder), NB_POPULATION)]
        eleves = eleves_garder + nouveau_eleve
        eleves.sort(key=lambda x: x.score, reverse=False)
    return eleves


def main():
    fichier = open(FICHIER_CSV, 'r')
    lignes = fichier.readlines()

    noms_matieres = lignes[0].replace('\n', '').split(';')[3:]
    nb_eleves_matieres = lignes[1].replace('\n', '').split(';')[3:]

    eleve = Eleve()
    for ligne in lignes[2:]:
        option = ligne.replace('\n', '').split(';')
        noms = option[0]+";"+option[1]+";"+option[2]
        option = option[3:]
        spe = []
        for i in range(len(noms_matieres)):
            if (option[i] != '') and (int(option[i]) == 1):
                spe.append(i)
        while len(spe) < NB_GROUPES:
            spe.append(-1)
        eleve.matieres[noms] = spe

    for opt in range(len(noms_matieres)):
        tmp , classe = eleve.getNbEleve(opt, int(nb_eleves_matieres[opt]))
        Eleve.CONFIG[opt] = (classe, 0 if (classe == 0) else (tmp / classe), int(nb_eleves_matieres[opt]))
        print(noms_matieres[opt], ":", tmp, "soit", classe, "classe(s)")

    population = [eleve.getRandom() for _ in range(NB_POPULATION)]
    population.sort(key=lambda x: x.score, reverse=False)
    i = 0
    print('Générations : %6d' %i, population[0].stat(), 'Meilleur score : %d' %population[0].score)
    
    solution = None
    while solution == None:
        try:
            i += NB_GENERATION
            population = evaluation_eleves(population)
            print('Générations : %6d' %i, population[0].stat(), 'Meilleur score : %d' %population[0].score)
            if population[0].score < 100:
                solution = population[0]
        except KeyboardInterrupt:
            break

    if solution:
        print('Une solution a été trouvé :')
    else:
        print('\nPas de solution trouvé :')
        solution = population[0]

    print('Générations : %6d' %i, solution.stat(), 'Meilleur score : %d' %solution.score)
    fichier = open('resultat.csv', 'w')
    fichier.write(solution.affiche(noms_matieres))
    fichier.close()

if __name__ == '__main__':
    main()