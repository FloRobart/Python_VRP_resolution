import view.view as view
import model.model as model

class Controller:
    def __init__(self):
        self.model = model.Model(self)
        self.view = view.View(self)

    def executeCPLEX(self, lien):
        self.model.executeCPLEX(lien)


if __name__ == "__main__":
    controller = Controller()
