
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

class Placement:
    def __init__(self,code: int, pawnType: int, location: Location):
        self.code = code
        self.pawnType = pawnType
        self.location = location

    def getLocation(self) -> Location:
        return self.location

    def getPawnType(self) -> int:
        return self.pawnType
    
    def getPawnSymbol(self) -> str:
        print(self.pawnType)
        if self.pawnType == 0:
            return "X"
        elif self.pawnType == 1:
            return "O"
        return "N"
    
    def getRoomCode(self) -> int:
        return self.code
