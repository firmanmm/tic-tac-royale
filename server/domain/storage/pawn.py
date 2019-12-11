import typing as typ
import server.domain.model.pawn as pawnMod
import server.domain.model.location as locMod

class IPawnStorage:

    def getPawn(self, location: locMod.Location) -> pawnMod.Pawn:
        raise NotImplementedError()

    def setPawn(self, location: locMod.Location, pawn: pawnMod.Pawn):
        raise NotImplementedError()