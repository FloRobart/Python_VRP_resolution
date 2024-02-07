import view.view as view

class Controller:
    def __init__(self):
        self.view = view.View(self)

if __name__ == "__main__":
    controller = Controller()
