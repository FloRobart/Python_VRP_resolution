import ast
import subprocess

import cplex
from cplex.exceptions import CplexError
from docplex.mp.model import Model
import numpy as np
import os

from docplex.mp.model_reader import ModelReader


class Metier:

    def __init__(self, ctrl):
        self.ctrl = ctrl

    def executeCPLE(self, fichierDat):
        # Créer une instance du problème
        prob = cplex.Cplex()

        # Charger le modèle depuis le fichier .mod
        fichierMod = os.getcwd() + "/model/sac_a_dos.mod"

        cplex_executable = ""  # Remplacez par le chemin correct

        # Appeler oplrun pour convertir le fichier .mod en .mps
        subprocess.run([cplex_executable, "-e", fichierMod])

        prob.read(fichierMod)

        # Charger les données depuis le fichier .dat
        prob.read(fichierDat)

        # Résoudre le problème
        try:
            prob.solve()
            # Afficher les résultats
            print("Solution status: ", prob.solution.get_status())
            print("Objective value: ", prob.solution.get_objective_value())
            print("Solution: ", prob.solution.get_values())

        except CplexError as exc:
            print(exc)

    def read_dat(self, file_path):

        with open(file_path, 'r') as file:
            for line in file:
                cleaned_line = line.replace(';', '')

                if line.startswith("nombreNode"):
                    nombreNode = int(cleaned_line.split(" = ")[1])
                elif line.startswith("demande"):
                    demande = [int(num) for num in cleaned_line.split() if num.isdigit()]
                elif line.startswith("Q"):
                    Q = int(cleaned_line.split(" = ")[1])
                elif line.startswith("V"):
                    V = int(cleaned_line.split(" = ")[1])
                elif line.startswith("dist"):
                    # Lire toutes les lignes de la matrice
                    dist_lines = []
                    while not line.endswith('\n'):
                        dist_lines.append(cleaned_line.split(" = ")[1].strip('[]'))
                        line = next(file)

                    # Retirer la virgule à la fin de chaque ligne si présente
                    dist_lines = [row.rstrip(',') for row in dist_lines]
                    dist = np.array([list(map(float, row.split())) for row in dist_lines])

        return {"nombreNode": nombreNode, "demande": demande, "Q": Q, "V": V, "dist": dist}

    def read_dat_file(self, file_path):
        # Extraction des informations
        # Lecture des données du fichier
        with open(file_path, 'r') as file:
            lines = file.readlines()

        nb_objets = int(lines[0].split('=')[1].strip())
        poids_objets = list(map(int, lines[1].split('=')[1].strip('[]').split(',')))
        valeurs_objets = list(map(int, lines[2].split('=')[1].strip('[]').split(',')))
        p_max = int(lines[3].split('=')[1].strip())

        return nb_objets, poids_objets, valeurs_objets, p_max

    def executeCPLEX(self, lien):

        # Charger les données depuis le fichier .dat
        data = self.read_dat_file(lien)

        # Accéder aux données extraites


        # Création du modèle
        mdl = Model(name='sac_a_dos')

        # Lecture du modèle OPL depuis le fichier .mod
        fichierMod = os.getcwd() + "/model/sac_a_dos.mod"
        model_reader = ModelReader()
        model_reader.read(fichierMod)

        # Résolution du modèle
        mdl.solve()


        # Affichage des résultats
        mdl.print_solution()