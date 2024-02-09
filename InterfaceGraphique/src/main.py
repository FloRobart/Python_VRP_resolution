import view.view as view
import model.metier as metier

class Controller:
    def __init__(self):
        self.metier = metier.Metier(self)
        self.view = view.View(self)

    def executeCPLEX(self, lien):
        self.metier.executeCPLEX(lien)


if __name__ == "__main__":
    controller = Controller()
