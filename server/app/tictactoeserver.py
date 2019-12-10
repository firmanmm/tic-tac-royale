import server.app.server as serverMod
import server.app.storage.pawn as pawnStorMod
import server.app.storage.placement as placeStorMod
import server.app.storage.room as roomStorMod

import server.domain.model.placement as placMod
import server.domain.model.pawn as pawnMod

import server.domain.usecase.create_room as ucCrateRoomMod
import server.domain.usecase.join_room as ucJoinRoomMod
import server.domain.usecase.list_placement as ucListPlacementMod
import server.domain.usecase.place_pawn as ucPlacePawnMod
import server.domain.model.tictactoe as tttMod

import Pyro4
import json
import typing as typ
import traceback
import threading as threadMod

class TicTacToeServer:
    def __init__(self, host, port, identifier="main-", syncServer: typ.Sequence[str] = []):
        placementStorage = placeStorMod.PlacementStorage()
        roomStorage = roomStorMod.RoomStorage()
        self.host = host
        self.port = port

        self.lock = threadMod.Lock()
        self.identifier = identifier

        self.ticTacToe = tttMod.TicTacRoyale(placementStorage, roomStorage)
        self.server = serverMod.Server(host, port, identifier)

        self.ucCreateRoom = ucCrateRoomMod.CreateRoom(self.ticTacToe)
        self.ucJoinRoom = ucJoinRoomMod.JoinRoom(self.ticTacToe)
        self.ucListPlacement = ucListPlacementMod.ListPlacement(self.ticTacToe)
        self.ucPlacePawn = ucPlacePawnMod.PlacePawn(self.ticTacToe)

        self.syncServer : typ.Sequence[TicTacToeServer] = list()
        for server in syncServer:
            self.registerListener(server)       
        self.sync()
        



    def start(self):
        self.server.Start([self])

    def createRoom(self) -> int:
        print("Create Room Requested")
        try:
            self.acquireGlobalLock()
            room = self.ucCreateRoom.Create()
            try:
                for server in self.syncServer:
                    server.createNamedRoom(room.getCode())
            except Exception as e:
                pass
            self.releaseGlobalLock()
            return self._createSuccess(room.getCode())
        except Exception as e:
            self.releaseGlobalLock()
            return self._createError(e)
    
    def createNamedRoom(self, code: int):
        self.ucCreateRoom.CreateByCode(code)

    def joinRoom(self, code: int, cascade: bool = True) -> int:
        print("Join Room Requested")
        try:
            if cascade:
                self.acquireGlobalLock()
            pawnType = self.ucJoinRoom.Join(code)
            if cascade:
                try:
                    for server in self.syncServer:
                        server.joinRoom(code, False)
                except Exception as e:
                    pass
            if cascade:
                self.releaseGlobalLock()
            return self._createSuccess(pawnMod.PawnType.toInt(pawnType))
        except Exception as e:
            self.releaseGlobalLock()
            return self._createError(e)

    def listPlacement(self, hashState: int, lock: bool = True) -> typ.Sequence[typ.Dict[str, typ.Any]]:
        print("List Placement Requested")
        try:
            if lock:
                self.acquireGlobalLock()
            placements = self.ucListPlacement.List(hashState)
            processedPlacement : typ.Sequence[typ.Dict[str, typ.Any]] = list()
            for placement in placements:
                pawn = placement.getPawn()
                room = placement.getRoom()
                location = pawn.getLocation()
                processedPlacement.append({
                    "type" : pawnMod.PawnType.toInt(pawn.getType()),
                    "room" : {
                        "code" : room.getCode(),
                        "winner": pawnMod.PawnType.toInt(room.getWinner()),
                        "lastActivityX": room.getLastActivityX(),
                        "lastActivityO": room.getLastActivityO(),
                    },
                    "location": {
                        "x" : location.getX(),
                        "y" : location.getY(),
                    }
                })
            if lock:
                self.releaseGlobalLock()
            return self._createSuccess({
                "placements": processedPlacement,
                "hashState": self.ticTacToe.getHashState(),
            })
        except Exception as e:
            if lock:
                self.releaseGlobalLock()
            return self._createError(e)
    
    def placePawn(self, code: int, posX: int, posY: int, pawnType: int, cascade: bool = True) -> bool:
        print("Place Pawn Requested")
        try:
            realPawnType = pawnMod.PawnType.fromInt(pawnType)
            if realPawnType is None:
                raise Exception("Wrong Pawn Type")
            if cascade:
                self.acquireGlobalLock()
            winner = self.ucPlacePawn.Place(code, posX, posY, realPawnType)
            if cascade:
                try:
                    for server in self.syncServer:
                        server.placePawn(code, posX, posY, pawnType, False)
                except Exception as e:
                    pass
            if cascade:
                self.releaseGlobalLock()
            return self._createSuccess(pawnMod.PawnType.toInt(winner))
        except Exception as e:
            self.releaseGlobalLock()
            return self._createError(e)

    def _createError(self, exception : Exception) -> str:
        traceback.print_exc()
        print(str(exception))
        return json.dumps({
            "error": str(exception),
        })

    def _createSuccess(self, message: typ.Any) -> str:
        return json.dumps({
            "response": message,
        })

    def acquireLock(self):
        self.lock.acquire(True, 10)

    def releaseLock(self):
        self.lock.release()

    def acquireGlobalLock(self):
        self.acquireLock()
        deleteList = list()
        for server in self.syncServer:
            try:
                server.acquireLock()
            except Exception as e:
                deleteList.append(server)
                print("Exception detected when trying to acquire lock, %s" % (str(e)))
        for delete in deleteList:
            self.syncServer.remove(delete)
    
    def releaseGlobalLock(self):
        deleteList = list()
        for server in self.syncServer:
            try:
                server.releaseLock()
            except Exception as e:
                deleteList.append(server)
                print("Exception detected when trying to release lock, %s" % (str(e)))
        for delete in deleteList:
            self.syncServer.remove(delete)
        self.releaseLock()

    def sync(self):
        self.acquireGlobalLock()
        hashState = self.ticTacToe.getHashState()
        for server in self.syncServer:
            try:
                resp = server.listPlacement(hashState, False)
                placementList = self._parseResponse(resp)
                for placement in placementList["placements"]:
                    roomMap = placement["room"]
                    pawnType = placement["type"]
                    locationMap = placement["location"]

                    roomCode = roomMap["code"]
                    room = self.ticTacToe.findRoom(roomCode)
                    if room is None:
                        self.createNamedRoom(roomCode)
                        room = self.ticTacToe.findRoom(roomCode)
                    self.placePawn(room.getCode(), locationMap["x"], locationMap["y"], pawnType, False)
                    room.setLastActivityO(roomMap["lastActivityO"])
                    room.setLastActivityX(roomMap["lastActivityX"])
                break
            except Exception as e:
                print("Failed to perform recovery from a server, %s" % (str(e)))
        self.releaseGlobalLock()
    
    def _parseResponse(self, response: str) -> typ.Any:
        result : typ.Dict[str, typ.Any] = json.loads(response)
        if "error" in result:
            raise Exception(result["error"])
        return result["response"]

    def registerListener(self, name: str, cascade: bool = True):
        url = "PYRONAME:%s@%s:%d" % (name, self.host, self.port)
        proxy = Pyro4.Proxy(url)
        try:
            if cascade:
                proxy.registerListener(self.identifier+self.__class__.__name__, False)
                print("Registered listener for %s" % (url))
        except Exception as e:
            print("Failed to connect to %s, Exception %s" % (url, str(e)))
            return
        self.syncServer.append(proxy)

