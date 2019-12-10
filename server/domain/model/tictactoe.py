import server.domain.model.room as roomMod
import server.domain.model.location as locMod
import server.domain.model.pawn as pawnMod
import server.domain.model.placement as placMod

import server.domain.storage.pawn as pawnStorMod
import server.domain.storage.room as roomStorMod
import server.domain.storage.placement as placStorMod

import typing as typ
import random

class TicTacRoyale:
    
    def __init__(self, placementStorage: placStorMod.IPlacementStorage, roomStorage: roomStorMod.IRoomStorage):
        self.rooms = roomStorage
        self.placements = placementStorage
        self.hashState = 0

    def createRoom(self) -> roomMod.Room:
        code = random.randint(0, 10000000)
        while self.findRoom(code) is not None:
            code = random.randint(0, 10000000)
        return self.createRoomByCode(code)
    
    def createRoomByCode(self, code: int) -> roomMod.Room:
        if self.findRoom(code) is not None:
            raise Exception("Room with code %d already exist" % (code))
        room = roomMod.Room(code)
        self.rooms.setRoom(code, room)
        return room

    def findRoom(self, code: int) -> roomMod.Room:
        return self.rooms.getRoom(code)

    def hasPawn(self, location: locMod.Location) -> bool:
        return self.getPlacement(location) is not None

    def getPlacement(self, location: locMod.Location) -> pawnMod.Pawn:
        return self.placements.getPlacement(location)

    def addPawn(self,room: roomMod.Room, pawn: pawnMod.Pawn) -> placMod.Placement:
        if not self.hasPawn(pawn.getLocation()):
            if room.getWinner() is None:
                if room.getLastTurn() is not pawn.getType():
                    placement = placMod.Placement(room, pawn)
                    self.placements.setPlacement(pawn.getLocation(), placement)
                    room.addPawn(pawn)
                    self._updateWinCondition(room, pawn)
                    self.hashState += 1
                    return placement
                else:
                    raise Exception("Waiting for opponents to move")
            else:
                raise Exception("This room already end")
        else:
            raise Exception("Location already used")

    def _updateWinCondition(self, room: roomMod.Room, pawn: pawnMod.Pawn):
        #Check winning condition, Crude but works :>
        #Check Horizontal
        ##Check left side
        count = -1
        for x in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() + x #TODO: Refactor Later
            pos = locMod.Location(xPos, pawnLoc.getY())
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
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
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break

        if count >= 5 :
            room.setWinner(pawn.getType())
            return

        #Check Vertical
        ##Check top side
        count = -1
        for y in range(5):
            pawnLoc = pawn.getLocation()
            yPos = pawnLoc.getY() + y #TODO: Refactor Later
            pos = locMod.Location(pawnLoc.getX(), yPos)
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
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
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break
        
        if count >= 5 :
            room.setWinner(pawn.getType())
            return

        #Check Diagonal Right
        ##Check top side
        count = -1
        for i in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() + i #TODO: Refactor Later
            yPos = pawnLoc.getY() + i #TODO: Refactor Later
            pos = locMod.Location(xPos, yPos)
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
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
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break
        
        if count >= 5 :
            room.setWinner(pawn.getType())
            return
        
        #Check Diagonal Left
        ##Check top side
        count = -1
        for i in range(5):
            pawnLoc = pawn.getLocation()
            xPos = pawnLoc.getX() - i #TODO: Refactor Later
            yPos = pawnLoc.getY() + i #TODO: Refactor Later
            pos = locMod.Location(xPos, yPos)
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
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
            posPlacement = self.placements.getPlacement(pos)
            if posPlacement is not None:
                if posPlacement.getRoom().getCode() is room.getCode():
                    posPawn = posPlacement.getPawn()
                    if posPawn.getType() is pawn.getType():
                        count += 1
                        continue
            break
        
        if count >= 5 :
            room.setWinner(pawn.getType())
            return

    def getHashState(self) -> int:
        return self.hashState
        
    def getPlacementSince(self, hashState: int) -> typ.Sequence[placMod.Placement]:
        return self.placements.listPlacement(self.hashState - hashState, hashState)