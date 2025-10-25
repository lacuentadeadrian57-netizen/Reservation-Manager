from datetime import datetime, timedelta
from manager import Local, Reservation, Manager

class App:
    def __init__(self):
        self.manager = Manager()

    def run(self):
        print(self.manager)

if __name__ == "__main__":
    app = App()
    app.run()