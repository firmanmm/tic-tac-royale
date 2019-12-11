import server.domain.model.room as roomMod

class IRoomStorage:

    def getRoom(self, code: int) -> roomMod.Room:
        raise NotImplementedError()

    def setRoom(self,code: int, room: roomMod.Room):
        raise NotImplementedError()