

class Eleves:

    def __init__(self, csv=''):
        self.matieres = {}
        self.score = None
        self.config = {}

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
                tmp , classe = self.getNbEleve(opt, int(nb_eleves_matieres[opt]))
                self.config[opt] = (classe, 0 if (classe == 0) else (tmp / classe), int(nb_eleves_matieres[opt]))
                print(noms_matieres[opt], ":", tmp, "soit", classe, "classe(s)")