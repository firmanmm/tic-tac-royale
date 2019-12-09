import server.domain.storage.placement as placStorMod
import server.domain.model.location as locMod
import server.domain.model.placement as placMod
import typing as typ

class PlacementStorage(placStorMod.IPlacementStorage):

    def __init__(self):
        self.sequence : typ.Sequence[placMod.Placement] = list()
        self.map : typ.Dict[locMod.Location, placMod.Placement] = dict()

    def getPlacement(self, location: locMod.Location) -> placMod.Placement:
        if location in self.map:
            return self.map[location]
        return None

    def setPlacement(self, location: locMod.Location, placement: placMod.Placement):
        self.map[location] = placement
        self.sequence.append(placement)
    
    def listPlacement(self, limit: int, offset: int) -> typ.Sequence[placMod.Placement]:
        if len(self.sequence) > limit + offset:
            raise Exception("Out Of Bound")
        return self.sequence[offset: offset + limit]