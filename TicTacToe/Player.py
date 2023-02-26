
class Player:

    def __init__(self, type):
        self.type = type
        self.cross = []
        self.circle = []

    def add_case(self, num):
        if type == 1:
            self.cross.append(num)
        elif type == 2:
            self.circle.append(num)