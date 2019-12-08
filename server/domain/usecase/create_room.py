import server.domain.model.tictactoe as tttMod
import server.domain.model.room as roomMod
import asyncio.locks as lockMod

class CreateRoom:

    def __init__(self, ticTacToe: tttMod.TicTacRoyale):
        self.tictactoe = ticTacToe

    def Create(self) -> roomMod.Room:
        room = self.tictactoe.createRoom()
        return room

