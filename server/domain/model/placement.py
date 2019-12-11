import server.domain.model.pawn as pawnMod
import server.domain.model.room as roomMod

class Placement:
    def __init__(self, room: roomMod.Room, pawn: pawnMod.Pawn):
        self.room = room
        self.pawn = pawn

    def getRoom(self) -> roomMod.Room:
        return self.room

    def getPawn(self) -> pawnMod.Pawn:
        return self.pawn