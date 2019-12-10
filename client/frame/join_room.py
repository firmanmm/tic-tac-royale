import tkinter as tki
import tkinter.font as tkf
import tkinter.ttk as ttk
import client.asset.font as fontMod
import client.frame.base as baseMod
import client.frame.stack as stackMod
import client.client as clientMod
import tkinter.messagebox as msgMod

class JoinRoom(baseMod.IBase):
    def __init__(self, stackFrame: stackMod.FrameStack, client: clientMod.TicTacToeClient):
        self.client = client
        self.stack = stackFrame
        root = stackFrame.getTkInstance()
        stackFrame.registerNamed(self)
        self.frame = ttk.Frame(root, width=800, height=600)
        title = ttk.Label(
            self.frame, 
            text="Tic Tac Royale",
            font=fontMod.Font.TitleFont)
        title.place(x=400-title.winfo_reqwidth()/2, y=20)
        exitBtn = tki.Button(self.frame, text="Kembali", width=20, command=self.stack.pop)
        exitBtn.place(x=800 - exitBtn.winfo_reqwidth() - 20, y=600 - exitBtn.winfo_reqheight() - 20)
        codeFrame = self.buildCodeFrame()
        codeFrame.place(x=400-codeFrame.winfo_reqwidth()/2, y=100)
        self.frame.grid()
        self.hide()
        
    def buildCodeFrame(self) -> tki.Widget:
        codeFrame = ttk.Frame(self.frame)
        self.entryVar = tki.IntVar(codeFrame, value=0, name="entryFrame")
        codeEntry = ttk.Entry(codeFrame, width=20, textvariable=self.entryVar, font=fontMod.Font.NormalFont)
        codeEntry.grid(column=1, row=0, columnspan=2)
        codeSymbol = ttk.Label(
            codeFrame,
            text="Kode",
            font=fontMod.Font.NormalFont
            )
        codeSymbol.grid(column=0, row=0, padx=10)
        codeSymbol.update()
        joinBtn = tki.Button(codeFrame, text="Ikuti", width=20, command=self.joinRoom)
        joinBtn.grid(column=3, row=0, padx=10)
        codeFrame.update()
        return codeFrame

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def joinRoom(self):
        code = self.entryVar.get()
        print("Trying to Join %d" % (code))
        try:
            self.client.joinRoom(code)
            self.stack.pushNamed("BoardPlayer")
        except Exception as e:
            msgMod.showerror("Error", str(e))