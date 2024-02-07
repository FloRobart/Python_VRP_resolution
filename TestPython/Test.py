#=================================#
# Test d'interface graphique vide #
#=================================#
# # importations à faire pour la réalisation d'une interface graphique
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget

# # Première étape : création d'une application Qt avec QApplication
# #    afin d'avoir un fonctionnement correct avec IDLE ou Spyder
# #    on vérifie s'il existe déjà une instance de QApplication
# app = QApplication.instance() 
# if not app: # sinon on crée une instance de QApplication
#     app = QApplication(sys.argv)

# # création d'une fenêtre avec QWidget dont on place la référence dans fen
# fen = QWidget()

# # la fenêtre est rendue visible
# fen.show()

# # exécution de l'application, l'exécution permet de gérer les événements
# app.exec_()



#=====================================================#
# Test : fixer la position et la taille de la fenêtre #
#=====================================================#
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget

# app = QApplication.instance() 
# if not app:
#     app = QApplication(sys.argv)

# fen = QWidget()

# # on donne un titre à la fenêtre
# fen.setWindowTitle("Premiere fenetre")

# # on fixe la taille de la fenêtre
# fen.resize(500,250)

# # on fixe la position de la fenêtre
# fen.move(300,50)

# fen.show()

# app.exec_()



#==================================#
# Test : Création de deux fenêtres #
#==================================#
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget

# app = QApplication.instance() 
# if not app:
#     app = QApplication(sys.argv)

# fen1 = QWidget()
# fen1.setWindowTitle("Fenetre 1")
# fen1.resize(500,250)
# fen1.move(300,50)
# fen1.show()

# fen2 = QWidget()
# fen2.setWindowTitle("Fenetre 2")
# fen2.resize(400,300)
# fen2.move(200,150)
# fen2.show()

# app.exec_()



#=============================================#
# Test : Création d’une fenêtre personnalisée #
#=============================================#
# import sys
# from PyQt5.QtWidgets import QApplication, QWidget

# class Fenetre(QWidget):
#     def __init__(self):
#         QWidget.__init__(self)
#         self.setWindowTitle("Ma fenetre")

# app = QApplication.instance() 
# if not app:
#     app = QApplication(sys.argv)
    
# fen = Fenetre()
# fen.show()

# app.exec_()



#======================================================================#
# Test : Gestion de l’appui sur un bouton de la souris dans la fenêtre #
#======================================================================#
import sys
from PyQt5.QtWidgets import QApplication, QWidget

class Fenetre(QWidget):
    def __init__(self):
        QWidget.__init__(self)
        self.setWindowTitle("Ma fenetre")

    def mousePressEvent(self, event):
        print("appui souris")

app = QApplication.instance() 
if not app:
    app = QApplication(sys.argv)
    
fen = Fenetre()
fen.show()

app.exec_()