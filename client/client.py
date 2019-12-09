import Pyro4
import os
import json
import base64
import client.model as modelMod
import typing as typ

class Client:
    def __init__(self, host, port, identifier = "main-"):
        self.host = host
        self.port = port
        self.identifier = identifier
        self.objects = dict()

    def Start(self, remoteObjects):
        for obj in remoteObjects:
            url = "PYRONAME:%s%s@%s:%d" % (self.identifier, obj, self.host, self.port)
            self.objects[obj] = Pyro4.Proxy(url)

    def GetObject(self, name):
        return self.objects[name]


class TicTacToeClient:

    def __init__(self, host: str, port: int, identifier="main-"):
        self.client = Client(host, port, identifier)
        self.client.Start(["TicTacToeServer"])
        self.server = self.client.GetObject("TicTacToeServer")
        self.pawnType : int = None
        self.roomCode : int = None
        self.hashState : int = 0
        self.placementList : typ.Sequence[modelMod.Placement] = list()
        self.placementHistory : typ.Sequence[modelMod.Placement] = list()
        self.placementMap : typ.Dict[modelMod.Location, modelMod.Placement] = dict()

    def getRoomCode(self):
        return self.roomCode

    def placePawn(self, posX: int, posY: int) -> bool:
        resp = self.server.placePawn(self.roomCode, posX, posY, self.pawnType)
        resp = self._parseResponse(resp)
        return resp is self.pawnType

    def createRoom(self):
        resp = self.server.createRoom()
        self.roomCode = self._parseResponse(resp)
        self.joinRoom(self.roomCode)

    def joinRoom(self, code: int):
        resp = self.server.joinRoom(code)
        self.pawnType = self._parseResponse(resp)
        self.roomCode = code
    
    def synchronize(self):
        resp = self.server.listPlacement(self.hashState)
        parsedResp = self._parseResponse(resp)
        self.hashState = parsedResp["hashState"]
        for rawPlacement in parsedResp["placements"]:
            roomCode = rawPlacement["room"]["code"]
            pawnType = rawPlacement["type"]
            xPos = rawPlacement["location"]["x"]
            yPos = rawPlacement["location"]["y"]
            location = modelMod.Location(xPos, yPos)
            placement = modelMod.Placement(roomCode, pawnType, location)
            if roomCode == self.roomCode:
                self.placementHistory.append(placement)
            self.placementList.append(placement)
            self.placementMap[location] = placement

    def getPawnAtCoordinate(self, xPos: int, yPos: int):
        location = modelMod.Location(xPos, yPos)
        if location in self.placementMap:
            return self.placementMap[location]
        return None

    def getPawnType(self) -> int:
        return self.pawnType

    def _parseResponse(self, response: str) -> typ.Any:
        result : typ.Dict[str, typ.Any] = json.loads(response)
        if "error" in result:
            raise Exception(result["error"])
        return result["response"]

    def getPlacementHistory(self) -> typ.Sequence[modelMod.Placement]:
        return self.placementHistory