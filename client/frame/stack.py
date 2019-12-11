import client.frame.base as baseMod
import typing as typ
import tkinter as tki

class FrameStack():

    def __init__(self, tkInstance: tki.Tk):
        self.stack : typ.Sequence[baseMod.IBase] = list()
        self.tkInstance = tkInstance
        self.namedFrame : typ.Dict[str, baseMod.IBase] = dict()

    def push(self, frame: baseMod.IBase):
        if len(self.stack) > 0:
            self.stack[len(self.stack) - 1].hide()
        self.stack.append(frame)
        frame.show()

    def pushNamed(self, frameName: str):
        if frameName in self.namedFrame:
            frame = self.namedFrame[frameName]
            self.push(frame)
        else:
            raise Exception("Frame Name Not Found")

    def registerNamed(self, frame: baseMod.IBase):
        self.namedFrame[frame.__class__.__name__] = frame

    def pop(self):
        if len(self.stack) > 1:
            frame = self.stack.pop()
            frame.hide()
            self.stack[len(self.stack) - 1].show()
        else:
            self.tkInstance.destroy()
    
    def getTkInstance(self) -> tki.Tk:
        return self.tkInstance
