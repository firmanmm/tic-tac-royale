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

    def createRoom(self) -> int:
        try:
            room = self.ucCreateRoom.Create()
            return self._createSuccess(room.getCode())
        except Exception as e:
            return self._createError(e)

    def joinRoom(self, code: int) -> int:
        try:
            pawnType = self.ucJoinRoom.Join(code)
            return self._createSuccess(pawnMod.PawnType.toInt(pawnType))
        except Exception as e:
            return self._createError(e)

    def listPlacement(self, hashState: int) -> typ.Sequence[typ.Dict[str, typ.Any]]:
        try:
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
            return self._createSuccess({
                "placements": processedPlacement,
                "hashState": self.ticTacToe.getHashState(),
            })
        except Exception as e:
            return self._createError(e)
    
    def placePawn(self, code: int, posX: int, posY: int, pawnType: int) -> bool:
        try:
            realPawnType = pawnMod.PawnType.fromInt(pawnType)
            if realPawnType is None:
                raise Exception("Wrong Pawn Type")
            winner = self.ucPlacePawn.Place(code, posX, posY, realPawnType)
            return self._createSuccess(pawnMod.PawnType.toInt(winner))
        except Exception as e:
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

    


server = TicTacToeServer("localhost", 7777)
server.start()