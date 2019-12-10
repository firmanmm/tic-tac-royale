import tkinter as tki
import tkinter.font as tkf
import tkinter.ttk as ttk
import client.asset.font as fontMod
import client.frame.base as baseMod
import client.frame.stack as stackMod
import client.client as clientMod
import tkinter.messagebox as msgBoxMod

class Home(baseMod.IBase):

    def __init__(self, stackFrame: stackMod.FrameStack, client: clientMod.TicTacToeClient):
        self.client = client
        root = stackFrame.getTkInstance()
        self.stack = stackFrame
        stackFrame.registerNamed(self)
        self.frame = ttk.Frame(root, width=800, height=600)
        title = ttk.Label(
            self.frame, 
            text="Tic Tac Royale",
            font=fontMod.Font.TitleFont)
        title.place(x=400-title.winfo_reqwidth()/2, y=20)
        nameFrame = self.buildNameFrame()
        nameFrame.place(x=400-nameFrame.winfo_reqwidth()/2, y=100)
        menuFrame = self.buildMenuFrame()
        menuFrame.place(x=400-menuFrame.winfo_reqwidth()/2, y=200)
        exitBtn = tki.Button(self.frame, text="Keluar", width=20, command=self.stack.pop)
        exitBtn.place(x=800 - exitBtn.winfo_reqwidth() - 20, y=600 - exitBtn.winfo_reqheight() - 20)
        self.frame.grid()
        self.hide()

    def buildNameFrame(self) -> tki.Widget:
        nameFrame = ttk.Frame(self.frame)
        nameEntry = ttk.Entry(nameFrame, width=20, font=fontMod.Font.NormalFont)
        nameEntry.grid(column=1, row=0, columnspan=2)
        nameLabel = ttk.Label(
            nameFrame,
            text="Name",
            font=fontMod.Font.NormalFont
            )
        nameLabel.grid(column=0, row=0, padx=10)
        nameLabel.update()
        return nameFrame

    def buildMenuFrame(self) -> tki.Widget:
        menuFrame = ttk.Frame(self.frame)
        newRoomBtn = tki.Button(menuFrame, text="Buat Ruangan", width=30, height=1, font=fontMod.Font.MenuButtonFont, command=self.createRoom)
        newRoomBtn.pack(pady=5)
        joinRoomBtn = tki.Button(menuFrame, text="Ikuti Ruangan", width=30, height=1, font=fontMod.Font.MenuButtonFont, command=self.joinRoom)
        joinRoomBtn.pack(pady=5)
        viewBtn = tki.Button(menuFrame, text="Penonton", width=30, height=1, font=fontMod.Font.MenuButtonFont, command=self.watchRoom)
        viewBtn.pack(pady=5)
        menuFrame.update()
        return menuFrame

    def show(self):
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()

    def createRoom(self):
        try:
            self.client.createRoom()
            self.stack.pushNamed("CreateRoom")
        except Exception as e:
            msgBoxMod.showerror("Error", str(e))

    def joinRoom(self):
        self.stack.pushNamed("JoinRoom")
    
    def watchRoom(self):
        self.stack.pushNamed("WatchRoom")
