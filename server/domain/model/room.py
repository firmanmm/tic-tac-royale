import server.domain.model.pawn as pawnMod
import server.domain.storage.placement as placStorMod
import server.domain.model.location as locMod
import typing as typ
import datetime

class Room:
    def __init__(self, code: int, placementStorage : placStorMod.IPlacementStorage):
        self.code = code
        self.lastPawnActivityX = datetime.datetime.now() - datetime.timedelta(hours=2)
        self.lastPawnActivityO = datetime.datetime.now() - datetime.timedelta(hours=2)
        self.placementStorage = placementStorage
        self.winner : pawnMod.PawnType = None
        self.lastTurn : pawnMod.PawnType = None

    def addPawn(self, pawn: pawnMod.Pawn):
        self.pawnStorage.setPawn(pawn.getLocation(), pawn)
        self.refreshTime(pawn.getType())
        self.lastTurn = pawn.getType()

        #Check winning condition, Crude but works :>
        #Check Horizontal
        ##Check left side
        count = -1
        for x in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() + x #TODO: Refactor Later
            pos = locMod.Location(xPos, pawnLoc.getY())
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break

        ##Check right side
        for x in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() - x #TODO: Refactor Later
            pos = locMod.Location(xPos, pawnLoc.getY())
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break

        if count >= 5 :
            self.winner = pawn.getType()
            return

        #Check Vertical
        ##Check top side
        count = -1
        for y in range(5):
            pawnLoc = pawn.getLocation()
            yPos = pawnLoc.getY() + y #TODO: Refactor Later
            pos = locMod.Location(pawnLoc.getX(), yPos)
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break

        ##Check bottom side
        for y in range(5):
            pawnLoc = pawn.getLocation()
            yPos = pawnLoc.getY() - y #TODO: Refactor Later
            pos = locMod.Location(pawnLoc.getX(), yPos)
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break
        
        if count >= 5 :
            self.winner = pawn.getType()
            return

        #Check Diagonal Right
        ##Check top side
        count = -1
        for i in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() + i #TODO: Refactor Later
            yPos = pawnLoc.getY() + i #TODO: Refactor Later
            pos = locMod.Location(xPos, yPos)
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break

        ##Check bottom side
        for i in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() - i #TODO: Refactor Later
            yPos = pawnLoc.getY() - i #TODO: Refactor Later
            pos = locMod.Location(xPos, yPos)
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break
        
        if count >= 5 :
            self.winner = posPawn.getType()
            return
        
        #Check Diagonal Left
        ##Check top side
        count = -1
        for i in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() - i #TODO: Refactor Later
            yPos = pawnLoc.getY() + i #TODO: Refactor Later
            pos = locMod.Location(xPos, yPos)
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break

        ##Check bottom side
        for i in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() + i #TODO: Refactor Later
            yPos = pawnLoc.getY() - i #TODO: Refactor Later
            pos = locMod.Location(xPos, yPos)
            posPlacement = self.placementStorage.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().code is self.code:
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break
        
        if count >= 5 :
            self.winner = posPawn.getType()
            return

        
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