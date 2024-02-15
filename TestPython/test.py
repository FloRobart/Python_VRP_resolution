import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QHBoxLayout, QFileDialog, QTextEdit, QWidget, QShortcut, QLabel
from PyQt5.QtGui import QKeySequence
from PyQt5.QtCore import Qt


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
        self.select_button = QPushButton('Select Text File')
        self.save_button = QPushButton('Save')
        self.clear_button = QPushButton('Clear')

        # Create shortcuts
        save_shortcut = QShortcut(QKeySequence('Ctrl+S'), self)
        save_shortcut.activated.connect(self.save_file)

        self.select_button.clicked.connect(self.show_file_dialog)
        self.save_button.clicked.connect(self.save_file)

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
        layout.addWidget(self.clear_button)

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
                self.text_edit_read_solution.setPlainText(file_content)
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
                    file.write(self.text_edit_read_solution.toPlainText())

                self.label.setStyleSheet("QLabel { color : green; }");
                self.label.setText(f'Fichier sauvegarder : {file_name}')
                self.read_and_display_file(file_name)
            except Exception as e:
                self.label.setStyleSheet("QLabel { color : red; }");
                self.label.setText(f'Erreur lors de l\'enregistrement du fichier : {str(e)}')
                print(e)

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
