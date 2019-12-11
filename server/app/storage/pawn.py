import typing as typ
import server.domain.model.pawn as pawnMod
import server.domain.model.location as locMod
import server.domain.storage.pawn as pawnStorMod

class PawnStorage(pawnStorMod.IPawnStorage):

    def __init__(self):
        self.map = typ.Dict[locMod.Location, pawnMod.Pawn]()

    def getPawn(self, location: locMod.Location) -> pawnMod.Pawn:
        if location in self.map:
            return self.map.get(location)
        return None

    def setPawn(self, location: locMod.Location, pawn: pawnMod.Pawn):
        self.map[location] = pawn 