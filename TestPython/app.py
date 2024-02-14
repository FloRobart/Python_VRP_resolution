import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QFileDialog, QLabel, QTextEdit, QWidget, QShortcut
from PyQt5.QtGui import QKeySequence


class FileSelectorApp(QMainWindow):
    def __init__(self):
        super(FileSelectorApp, self).__init__()

        self.setWindowTitle('Interface graphique pour le solveur CPlex')
        self.setGeometry(100, 100, 600, 400)

        # Create widgets
        self.label = QLabel('Fichier sélectionné : None')
        self.text_edit = QTextEdit()
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
        layout.addWidget(self.text_edit)
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
        file_name, _ = QFileDialog.getOpenFileName(self, "Sélectionner un fichier texte", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            self.label.setText(f'Fichier sélectionné : {file_name}')
            self.read_and_display_file(file_name)

    def read_and_display_file(self, file_name):
        try:
            with open(file_name, 'r') as file:
                file_content = file.read()
                self.text_edit.setPlainText(file_content)
        except Exception as e:
            self.text_edit.setPlainText(f'Erreur lors de la lecture du fichier : {str(e)}')

    def save_file(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_name, _ = QFileDialog.getSaveFileName(self, "Save Text File", "", "Text Files (*.txt);;All Files (*)", options=options)

        if file_name:
            try:
                with open(file_name, 'w') as file:
                    file.write(self.text_edit.toPlainText())
                self.label.setText(f'Fichier sauvegarder : {file_name}')
            except Exception as e:
                self.label.setText(f'Erreur lors de l\'enregistrement du fichier : {str(e)}')

    def solve(self):
        print('Résolution...')
        # TODO : transformer les coordonnées x,y en matrice d'adjacence
        # TODO : Donner la matrice d'adjacence à la partie de Duc


def main():
    app = QApplication(sys.argv)
    window = FileSelectorApp()
    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
