import server.domain.model.room as roomMod
import server.domain.storage.room as roomStorMod
import typing as typ

class RoomStorage(roomStorMod.IRoomStorage):

    def __init__(self):
        self.map : typ.Dict[int, roomMod.Room] = dict()

    def getRoom(self, code: int) -> roomMod.Room:
        if code in self.map:
            return self.map[code]
        return None

    def setRoom(self, code: int, room: roomMod.Room):
        self.map[code] = room