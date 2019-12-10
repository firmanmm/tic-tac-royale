import server.domain.model.tictactoe as tttMod
import server.domain.model.room as roomMod
import server.domain.model.pawn as pawnMod
import server.domain.model.location as locMod
import server.domain.model.placement as placeMod
import asyncio.locks as lockMod

class PlacePawn:
    def __init__(self, tictactoe: tttMod.TicTacRoyale):
        self.tictactoe = tictactoe

    def Place(self, code: int, posX: int, posY: int, pawnType: pawnMod.PawnType) -> pawnMod.PawnType:
        location = locMod.Location(posX, posY)
        pawn = pawnMod.Pawn(pawnType, location)
        room = self.tictactoe.findRoom(code)
        if room is None:
            raise Exception("Room Not Found")
        self.tictactoe.addPawn(room, pawn)
        return room.getWinner()
