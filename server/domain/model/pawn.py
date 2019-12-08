import enum
import server.domain.model.location as locMod

class PawnType(enum.Enum):
    X = 0
    O = 1
    N = 2

class Pawn:
    def __init__(self, type: PawnType, location: locMod.Location):
        self.type = PawnType
        self.location = location
    
    def getType(self) -> PawnType:
        return self.type

    def getLocation(self) -> locMod.Location:
        return self.location