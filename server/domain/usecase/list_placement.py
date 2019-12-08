import server.domain.model.tictactoe as tttMod
import server.domain.model.room as roomMod
import server.domain.model.pawn as pawnMod
import server.domain.model.location as locMod
import server.domain.model.placement as placeMod

class ListPlacement:
    def __init__(self, tictactoe: tttMod.TicTacRoyale):
        self.tictactoe = tictactoe

    def List(self, hashState: int):
        currentState = self.tictactoe.getHashState()
        if hashState != currentState :
            return self.tictactoe.getPlacementSince(hashState)
        return None