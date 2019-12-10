import server.domain.model.pawn as pawnMod
import server.domain.model.location as locMod
import typing as typ
import datetime

class Room:
    def __init__(self, code: int):
        self.code = code
        self.lastPawnActivityX = datetime.datetime.now() - datetime.timedelta(hours=2)
        self.lastPawnActivityO = datetime.datetime.now() - datetime.timedelta(hours=2)
        self.winner : pawnMod.PawnType = None
        self.lastTurn : pawnMod.PawnType = None

    def addPawn(self, pawn: pawnMod.Pawn):
        self.refreshTime(pawn.getType())
        self.lastTurn = pawn.getType()

    def setWinner(self, pawn: pawnMod.PawnType):
        self.winner = pawn
        
    def getWinner(self) -> pawnMod.PawnType:
        return self.winner

    def getCode(self) -> int:
        return self.code

    def getAvailableSpot(self) -> pawnMod.PawnType:
        limitTime = datetime.datetime.now() - datetime.timedelta(minutes=1)
        if self.lastPawnActivityX < limitTime:
            self.refreshTime(pawnMod.PawnType.X)
            return pawnMod.PawnType.X
        elif self.lastPawnActivityO < limitTime:
            self.refreshTime(pawnMod.PawnType.O)
            return pawnMod.PawnType.O
        return None
    
    def refreshTime(self, pawnType: pawnMod.PawnType):
        if pawnType is pawnMod.PawnType.X:
            self.lastPawnActivityX = datetime.datetime.now()
        elif pawnType is pawnMod.PawnType.O:
            self.lastPawnActivityO = datetime.datetime.now()

    def getLastTurn(self) -> pawnMod.PawnType:
        return self.lastTurn

    def getLastActivityX(self) -> float:
        return datetime.datetime.timestamp(self.lastPawnActivityX)

    def getLastActivityO(self) -> float:
        return datetime.datetime.timestamp(self.lastPawnActivityO)

    def setLastActivityX(self, second: float):
        self.lastPawnActivityX = datetime.datetime.fromtimestamp(second)

    def setLastActivityO(self, second: float):
        self.lastPawnActivityO = datetime.datetime.fromtimestamp(second)