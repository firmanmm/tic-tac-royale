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

class TicTacToeServer:
    def __init__(self, host, port, identifier="main-"):
        placementStorage = placeStorMod.PlacementStorage()
        roomStorage = roomStorMod.RoomStorage()

        self.ticTacToe = tttMod.TicTacRoyale(placementStorage, roomStorage)
        self.server = serverMod.Server(host, port, identifier)

        self.ucCreateRoom = ucCrateRoomMod.CreateRoom(self.ticTacToe)
        self.ucJoinRoom = ucJoinRoomMod.JoinRoom(self.ticTacToe)
        self.ucListPlacement = ucListPlacementMod.ListPlacement(self.ticTacToe)
        self.ucPlacePawn = ucPlacePawnMod.PlacePawn(self.ticTacToe)

    def start(self):
        self.server.Start([self])

    def createRoom(self) -> str:
        try:
            room = self.ucCreateRoom.Create()
            return self._createSuccess(room.getCode())
        except Exception as e:
            return self._createError(e)

    def joinRoom(self, code: int):
        try:
            pawnType = self.ucJoinRoom.Join(code)
            return self._createSuccess(pawnType)
        except Exception as e:
            return self._createError(e)

    def listPlacement(self, hashState: int) -> typ.Sequence[placMod.Placement]:
        try:
            placements = self.ucListPlacement.List(hashState)
            return self._createSuccess(placements)
        except Exception as e:
            return self._createError(e)
    
    def placePawn(self, code: int, posX: int, posY: int, pawnType: int) -> bool:
        try:
            realPawnType : pawnMod.PawnType = None
            if pawnType == 0:
                realPawnType = pawnMod.PawnType.O
            elif pawnType == 1:
                realPawnType = pawnMod.PawnType.X
            if realPawnType is None:
                raise Exception("Wrong Pawn Type")
            winner = self.ucPlacePawn.Place(code, posX, posX, realPawnType)
            return self._createSuccess(winner)
        except Exception as e:
            return self._createError(e)

    def _createError(self, exception : Exception) -> str:
        return json.dumps({
            "error": exception,
        })

    def _createSuccess(self, message: typ.Any) -> str:
        return json.dumps({
            "response": message,
        })

    


server = TicTacToeServer("localhost", 7777)
server.Start()