import server.domain.model.tictactoe as tttMod
import server.domain.model.room as roomMod
import server.domain.model.pawn as pawnMod
import server.domain.model.location as locMod
import server.domain.model.placement as placeMod
import typing as typ

class ListPlacement:
    def __init__(self, tictactoe: tttMod.TicTacRoyale):
        self.tictactoe = tictactoe

    def List(self, hashState: int) -> typ.Sequence[placeMod.Placement] :
        currentState = self.tictactoe.getHashState()
        if hashState != currentState :
            return self.tictactoe.getPlacementSince(hashState)
        return list()