import sys
import numpy as np
import matplotlib.pyplot as plt

from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QWidget, QShortcut, QLabel
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt

from docplex.mp.model import Model


class FileSelectorApp(QMainWindow):
    def __init__(self):
        super(FileSelectorApp, self).__init__()

        self.setWindowTitle('Interface graphique pour le solveur CPlex')
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        self.label = QLabel('Aucun fichier sélectionné.')
        self.label.setStyleSheet("QLabel { color : black; }");
        self.text_edit_editable = QTextEdit()
        self.text_edit_read_solution = QTextEdit()
        self.text_edit_read_solution.setReadOnly(True)
        self.text_edit_editable.setPlainText("Solution...")
        self.select_button = QPushButton('Sélectionner un fichier texte contenant les coordonnées des points')
        self.save_button = QPushButton('Sauvegarder le fichier')
        self.solve_button = QPushButton('Résoudre le problème avec CPlex')

        # Create shortcuts
        save_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        save_shortcut.activated.connect(self.save_file)

        self.select_button.clicked.connect(self.show_file_dialog)
        self.save_button.clicked.connect(self.save_file)
        self.solve_button.clicked.connect(self.solve)

        # Create layout
        layout = QVBoxLayout()
        layout.addWidget(self.label)

        # Create a horizontal layout for the text edits
        text_edit_layout = QHBoxLayout()
        text_edit_layout.addWidget(self.text_edit_editable)
        text_edit_layout.addWidget(self.text_edit_read_solution)

        # Add the horizontal text edit layout to the main layout
        layout.addLayout(text_edit_layout)

        # Add buttons to layout
        layout.addWidget(self.select_button)
        layout.addWidget(self.save_button)
        layout.addWidget(self.solve_button)

        # Create central widget
        central_widget = QWidget()
        central_widget.setLayout(layout)

        # Set central widget
        self.setCentralWidget(central_widget)

    def show_file_dialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getOpenFileName(self, "Select Text File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            self.label.setStyleSheet("QLabel { color : black; }");
            self.label.setText(f'Fichier sélectionné : {file_name}')
            self.read_and_display_file(file_name)

    def read_and_display_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                file_content = file.read()
                self.text_edit_editable.setPlainText(file_content)
        except Exception as e:
            self.text_edit_editable.setPlainText(f'Error reading file: {str(e)}')
            self.text_edit_read_solution.setPlainText('')
            self.text_edit_editable.setEnabled(False)
            self.text_edit_read_solution.setEnabled(True)

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.text_edit_editable.toPlainText())

                self.label.setStyleSheet("QLabel { color : green; }");
                self.label.setText(f'Fichier sauvegarder : {file_name}')
            except Exception as e:
                self.label.setStyleSheet("QLabel { color : red; }");
                self.label.setText(f'Erreur lors de l\'enregistrement du fichier : {str(e)}')
                print(e)

    def solve(self):
        print('Résolution...')
        Xclient = []
        Yclient = []
        demandeClient = [0]
        
        lignes = self.text_edit_editable.toPlainText().split('\n')
        cpt = 0
        for ligne in lignes:
            if cpt == 0:
                temp = ligne.split(' ')
                C = int(temp[0])
                V = int(temp[1])

                cpt+=1
                continue

            if cpt == 1:
                Q = int(ligne)
                cpt+=1
                continue

            if cpt == 2:
                Xdepot = int(ligne.split(' ')[0])
                Ydepot = int(ligne.split(' ')[1])
                cpt+=1
                continue

            tab = ligne.split(' ')
            Xclient.append(int(tab[1]))
            Yclient.append(int(tab[2]))
            demandeClient.append(int(tab[3]))

            cpt+=1
        
        Vehicles = [i for i in range(1, V+1)]
        N = [i for i in range(1, C+1)]
        print(N)
        Vertices = [0] + N
        demande = demandeClient
        print(demande)
        loc_x = [Xdepot]+Xclient
        loc_y = [Ydepot]+Yclient
        print(loc_x)
        print(loc_y)
        
        # plt.scatter(loc_x[1:], loc_y[1:], c='b')
        # for i in N:
        #     plt.annotate('$n_%d=%d$' % (i, demande[i]), (loc_x[i]+2, loc_y[i]))
        # plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
        # plt.axis('equal')
        # plt.show()
        
        A = [(i, j) for i in Vertices for j in Vertices if i!=j]
        B = [(i, j, v) for i in Vertices for j in Vertices for v in Vehicles if i!=j]
        print(B)
        dist = {(i, j): np.hypot(loc_x[i]-loc_x[j], loc_y[i]-loc_y[j]) for i in Vertices for j in Vertices}
        print(dist)
        
        # Modélisation mathématique
        mdl = Model('CVRP')
        x = mdl.binary_var_dict(B, name='x')
        u = mdl.continuous_var_dict(N, ub=Q, name='u')
        
        mdl.minimize(mdl.sum(dist[i, j]*x[i, j,v]  for i, j,v in B))
        mdl.add_constraint(mdl.sum(x[0,j,v] for j in N for v in Vehicles)>=1)#Au moins 1 véhicules utilisés
        mdl.add_constraints(mdl.sum(x[j,0,v] for j in N)<=1 for v in Vehicles)#Les véhicules si il quitte le dépôt, il rentrera au dépôt à la fin
        mdl.add_constraints(mdl.sum(x[j,0,v] for j in N)==mdl.sum(x[0,j,v] for j in N) for v in Vehicles) #Les véhicules si il quitte le dépôt, il rentrera au dépôt à la fin
        #Tous les véhicules quittent la node qu'il a visité
        mdl.add_constraints(mdl.sum(x[j,i,v] for i in Vertices if i!=j)== mdl.sum(x[i,j,v] for i in Vertices if i!=j) for j in Vertices for v in Vehicles)
        #Chaque client est passé par exactement 1 fois
        mdl.add_constraints(mdl.sum(x[i,j,v] for v in Vehicles for i in Vertices if i!=j) == 1 for j in N)
        #La capacité ne doit pas être dépassé
        mdl.add_constraints(mdl.sum(demande[j]*x[i,j,v] for i in Vertices for j in N if i!=j)<=Q for v in Vehicles)
        mdl.add_constraints(u[j]-u[i] >= demande[j]-Q*(1-x[i,j,v]) for i in N for j in N for v in Vehicles if i!=j)
        mdl.add_constraints(u[i]<= Q for i in N)
        mdl.add_constraints(u[i] >= demande[i] for i in N)
        solution = mdl.solve(log_output=True)
        #add_contraint et add_contraints => for chaque
        
        print(solution)
        
        solution.solve_status
        
        active_arcs = [a for a in B if x[a].solution_value > 0.9]
        print (active_arcs)
        
        # Définition de couleurs aléatoires
        color = np.random.rand(len(Vehicles), 3)
        
        
        plt.scatter(loc_x[1:], loc_y[1:], c='b')
        for i in N:
            plt.annotate('$n_%d=%d$' % (i, demande[i]), (loc_x[i]+2, loc_y[i]))
        for i, j,v in active_arcs:
            plt.plot([loc_x[i], loc_x[j]], [loc_y[i], loc_y[j]], c=color[v-1], alpha=0.3)
        plt.plot(loc_x[0], loc_y[0], c='r', marker='s')
        plt.axis('equal')
        plt.show()


def main():
    app = QApplication(sys.argv)
    window = FileSelectorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
