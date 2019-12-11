import enum
import server.domain.model.location as locMod

class PawnType(enum.Enum):
    X = 0
    O = 1
    N = 2

    @classmethod
    def toInt(cls, pawnType) -> int:
        if pawnType is cls.X:
            return 0
        elif pawnType is cls.O:
            return 1
        elif pawnType is cls.N:
            return 2
        return None

    @classmethod
    def fromInt(cls, pawnInt: int):
        if pawnInt is 0:
            return cls.X
        elif pawnInt is 1:
            return cls.O
        elif pawnInt is 2:
            return cls.N
        return None

class Pawn:
    def __init__(self, pawnType: PawnType, location: locMod.Location):
        self.type = pawnType
        self.location = location
    
    def getType(self) -> PawnType:
        return self.type

    def getLocation(self) -> locMod.Location:
        return self.location