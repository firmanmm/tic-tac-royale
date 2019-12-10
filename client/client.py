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

    def __init__(self, host: str, port: int, identifier="main-", servers=[]):
        self.client = Client(host, port, identifier)
        self.client.Start(servers)
        self.servers = list()
        self.serverName = servers
        self.mainServer = None
        self.pawnType : int = None
        self.roomCode : int = None
        self.hashState : int = 0
        self.placementList : typ.Sequence[modelMod.Placement] = list()
        self.placementHistory : typ.Sequence[modelMod.Placement] = list()
        self.placementMap : typ.Dict[modelMod.Location, modelMod.Placement] = dict()
        self.refindServer(servers)

    def refindServer(self, servers: typ.Sequence[str]):
        for server in servers:
            serverProxy = self.client.GetObject(server)
            self.servers.append(serverProxy)

    def getRoomCode(self):
        return self.roomCode

    def placePawn(self, posX: int, posY: int) -> bool:
        server = self.getActiveServer()
        resp = server.placePawn(self.roomCode, posX, posY, self.pawnType)
        resp = self._parseResponse(resp)
        return resp is self.pawnType

    def createRoom(self):
        server = self.getActiveServer()
        resp = server.createRoom()
        self.roomCode = self._parseResponse(resp)
        self.joinRoom(self.roomCode)

    def joinRoom(self, code: int):
        server = self.getActiveServer()
        resp = server.joinRoom(code)
        self.pawnType = self._parseResponse(resp)
        self.roomCode = code
    
    def synchronize(self):
        server = self.getActiveServer()
        resp = server.listPlacement(self.hashState)
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

    def getActiveServer(self):
        if self.mainServer is not None:
            try:
                self.mainServer._pyroBind()
                return self.mainServer
            except Exception as e:
                self.mainServer = None

        if self.mainServer is None:
            deleteList = list()
            for server in self.servers:
                try:
                    server._pyroBind()
                    self.mainServer = server
                except Exception as e:
                    print(str(e))
                    deleteList.append(server)
                    pass
            for delete in deleteList:
                self.servers.remove(delete)
        
        if self.mainServer is not None:
            return self.mainServer
        
        self.refindServer(self.serverName)

        if self.mainServer is None:
            deleteList = list()
            for server in self.servers:
                try:
                    server._pyroBind()
                    self.mainServer = server
                except Exception as e:
                    print(str(e))
                    deleteList.append(server)
                    pass
            for delete in deleteList:
                self.servers.remove(delete)
        
        if self.mainServer is not None:
            return self.mainServer
        raise Exception("Failed To Connect to all server")

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