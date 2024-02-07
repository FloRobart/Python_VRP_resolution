import os.path

import dearpygui.dearpygui as dpg
from _cffi_backend import callback


class View:

    def __init__(self, ctrl):
        self.ctrl = ctrl
        #self.selected_file_path = None
        self.selected_file_path = os.path.expanduser('~') + ("/TP/s6/s6.01_developpement_avance/SAE/InterfaceGraphique"
                                                             "/src/ressource/voyageurdeCommerce.dat")

        dpg.create_context()
        dpg.create_viewport(title='Interface CPLEX', width=1200, height=600)

        # add a font registry
        with dpg.font_registry():
            #Pour ajouter de nouvelle police
            pass

        with dpg.file_dialog(directory_selector=False, show=False, callback=self.callback, id="file_dialog_id", width=800,
                             height=500):
            dpg.add_file_extension(".dat")
            dpg.add_file_extension("", color=(150, 255, 150, 255))

        with dpg.window(label="Choix de Fichier", width=600, height=600, no_close=True):
            dpg.add_text("Choisir un fichier de jeu de données")
            dpg.add_button(label="Choisir un Fichier", callback=lambda: dpg.show_item("file_dialog_id"))
            dpg.add_input_text(default_value="voyageurdeCommerce.dat", readonly=True,
                               source=self.selected_file_path, id="input_text_id")
            dpg.add_button(label="Executer le programme", callback=self.executeCPLEX)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    def callback(self, sender, app_data):
        cheminFichier = app_data.get("file_path_name")
        nomFichier = app_data.get("file_name")
        self.selected_file_path = cheminFichier
        dpg.set_value("input_text_id", nomFichier)

    def executeCPLEX(self):
        self.ctrl.executeCPLEX(self.selected_file_path)
