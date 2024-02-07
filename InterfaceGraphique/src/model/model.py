import subprocess

import cplex
from cplex.exceptions import CplexError
import os


class Model:

    def __init__(self, ctrl):
        self.ctrl = ctrl

    def executeCPLEX(self, fichierDat):
        # Créer une instance du problème
        prob = cplex.Cplex()

        # Charger le modèle depuis le fichier .mod
        fichierMod = os.getcwd() + "/model/voyageurdeCommerce.mod"

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
