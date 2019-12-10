class Location:
    def __init__(self, x : int, y : int):
        self.x = x
        self.y = y

    def getX(self) -> int:
        return self.x 

    def getY(self) -> int:
        return self.y

    def __eq__(self, value):
        return self.x == value.x and self.y == value.y

    def __hash__(self):
        return hash("%d %d" % (self.x, self.y))