import server.domain.model.tictactoe as tttMod
import server.domain.model.room as roomMod
import server.domain.model.pawn as pawnMod
import asyncio.locks as lockMod

class JoinRoom:
    def __init__(self, tictactoe: tttMod.TicTacRoyale):
        self.tictactoe = tictactoe

    def Join(self, code: int) -> pawnMod.PawnType:
        room = self.tictactoe.findRoom(code)
        if room is None:
            raise Exception("Room Not Found")
        spot = room.getAvailableSpot()
        return spot
