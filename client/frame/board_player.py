import tkinter as tki
import tkinter.font as tkf
import tkinter.ttk as ttk
import client.asset.font as fontMod
import client.frame.base as baseMod
import client.frame.stack as stackMod
import client.client as clientMod
import tkinter.messagebox as msgMod
import typing as typ
import traceback
import enum

class BoardType(enum.Enum):
    Empty = 0 
    Occupied = 1
    XPiece = 2
    OPiece = 3 

class GridListener():
    def __init__(self, x, y, callback):
        self.x = x
        self.y = y
        self.callback = callback
    
    def Handle(self):
        self.callback(self.x, self.y)

class BoardPlayer(baseMod.IBase):

    def __init__(self, stackFrame: stackMod.FrameStack, client: clientMod.TicTacToeClient):
        self.client = client
        stackFrame.registerNamed(self)
        self.stack = stackFrame
        root = stackFrame.getTkInstance()
        self.frame = ttk.Frame(root, width=800, height=600)
        boardFrame = self.buildBoardFrame()
        boardFrame.place(x=50, y=200)
        title = ttk.Label(
            self.frame, 
            text="Tic Tac Royale",
            font=fontMod.Font.TitleFont)
        title.place(x=400-title.winfo_reqwidth()/2, y=20)
        roomCode = ttk.Label(
            self.frame, 
            text="Goodluck!",
            font=fontMod.Font.NormalFont)
        roomCode.place(x=400-roomCode.winfo_reqwidth()/2, y=50)
        self.roomCodeLabel = roomCode
        locationFrame = self.buildLocationFrame()
        locationFrame.place(x=800-locationFrame.winfo_reqwidth()-20, y=100)

        historyFrame = self.buildHistoryFrame()
        historyFrame.place(x=800-locationFrame.winfo_reqwidth()-20, y=200)

        self.frame.grid()
        self.hide()

    def buildBoardFrame(self) -> ttk.Frame:
        self.board : typ.Sequence[typ.Sequence[tki.Button]] = list()
        boardFrame = ttk.Frame(self.frame, width=330, height=330)
        for i in range(11):
            self.board.append(list())
            for j in range(11):
                btnFrame = tki.Frame(boardFrame, width=30, height=30)
                btnFrame.grid_propagate(False)
                btnFrame.columnconfigure(0, weight=1)
                btnFrame.rowconfigure(0, weight=1)
                listener = GridListener(j, i, self.gridCallback)
                btnGrid = tki.Button(btnFrame, text=" ", font=fontMod.Font.PawnGridFont, background="white", command=listener.Handle)
                btnGrid.grid(sticky="wens")
                btnFrame.update()
                btnFrame.place(x=j*30, y=i*30)
                self.board[i].append(btnGrid)
        boardFrame.update()
        return boardFrame
    
    def buildHistoryFrame(self) -> ttk.Frame:
        self.histories : typ.Sequence[tki.Label] = list()
        historyFrame = ttk.Frame(self.frame, width=250, height=400)
        for i in range(10):
            textFrame = tki.Frame(historyFrame, width=200, height=30)
            textFrame.grid_propagate(False)
            textFrame.columnconfigure(0, weight=1)
            textFrame.rowconfigure(0, weight=1)
            textGrid = tki.Label(textFrame, text="", font=fontMod.Font.NormalFont)
            textGrid.grid(sticky="wens")
            textGrid.update()
            textFrame.update()
            textFrame.place(x=0, y=i*40)
            self.histories.append(textGrid)
        
        upBtnFrame = tki.Frame(historyFrame, width=50, height=200)
        upBtnFrame.grid_propagate(False)
        upBtnFrame.columnconfigure(0, weight=1)
        upBtnFrame.rowconfigure(0, weight=1)
        upBtn = tki.Button(upBtnFrame, text="UP", font=fontMod.Font.PawnGridFont, background="white", command=self.upHistory)
        upBtn.grid(sticky="wens")
        upBtnFrame.place(x=200,y=0)
        upBtnFrame.update()

        downBtnFrame = tki.Frame(historyFrame, width=50, height=200)
        downBtnFrame.grid_propagate(False)
        downBtnFrame.columnconfigure(0, weight=1)
        downBtnFrame.rowconfigure(0, weight=1)
        downBtn = tki.Button(downBtnFrame, text="DW", font=fontMod.Font.PawnGridFont, background="white", command=self.downHistory)
        downBtn.grid(sticky="wens")
        downBtnFrame.place(x=200,y=200)
        downBtnFrame.update()

        historyFrame.update()
        return historyFrame
        
    def buildLocationFrame(self) -> ttk.Frame:
        xVal = tki.IntVar(self.frame,0,"xCenter")
        yVal = tki.IntVar(self.frame,0,"yCenter")
        self.xLocation = xVal
        self.yLocation = yVal
        locationFrame = ttk.Frame(self.frame, width=200, height=100)
        xLabel = ttk.Label(locationFrame, text="X", font=fontMod.Font.NormalFont)
        xLabel.pack(padx=5,side=tki.LEFT)
        xEntryFrame = ttk.Frame(locationFrame, width=100, height=50)
        xEntryFrame.pack_propagate(False)
        xEntry = ttk.Entry(xEntryFrame, textvariable=xVal, font=fontMod.Font.NormalFont)
        xEntry.pack(side=tki.LEFT)
        xEntryFrame.pack(side=tki.LEFT)
        yLabel = ttk.Label(locationFrame, text="Y", font=fontMod.Font.NormalFont)
        yLabel.pack(padx=5,side=tki.LEFT)
        yEntryFrame = ttk.Frame(locationFrame, width=100, height=50)
        yEntryFrame.pack_propagate(False)
        yEntry = ttk.Entry(yEntryFrame, textvariable=yVal, font=fontMod.Font.NormalFont)
        yEntry.pack(side=tki.LEFT)
        yEntryFrame.pack(side=tki.LEFT)

        locBtnFrame = ttk.Frame(locationFrame, width=50, height=50)
        locBtnFrame.pack_propagate(False)
        locBtn = tki.Button(locBtnFrame, text="Change", font=fontMod.Font.NormalFont, command=self.changeCenter)
        locBtn.pack(side=tki.LEFT)
        locBtnFrame.pack(side=tki.LEFT, padx=5)

        locationFrame.update()
        return locationFrame

    
    def gridCallback(self, x, y):
        x = x - 5 + self.xLocation.get()
        y = -y + 5 + self.yLocation.get()
        try:
            if self.client.placePawn(x, y):
                msgMod.showinfo("Win", "Yes you win, Thank You!")
        except Exception as e:
            traceback.print_exc()
            msgMod.showerror("Error", str(e))
        print("Clicked : X : %d, Y : %d" % (x, y))
        self.client.synchronize()
        self.updateGrid()


    def updateGrid(self):
        print("Updating Grid Display")
        for i in range(11):
            for j in range(11):
                grid = self.board[i][j]
                symbol = " "
                xPos = j - 5 + self.xLocation.get()
                yPos = -i + 5 + self.yLocation.get()
                pawn = self.client.getPawnAtCoordinate(xPos, yPos)
                if pawn is not None:
                    loc = pawn.getLocation()

                    print("X > %d, Y > %d || XPos %d, YPos %d" % (loc.getX(), loc.getY(), xPos, yPos))
                    symbol = pawn.getPawnSymbol()
                grid.configure(text=symbol)

    def upHistory(self):
        print("History Up")

    def downHistory(self):
        print("History Down")

    def changeCenter(self):
        print("Center Changed To X : %d and Y : %d" % (self.xLocation.get(), self.yLocation.get()))

    def show(self):
        self.roomCodeLabel.configure(text="Room : %d" % (self.client.getRoomCode()))
        self.frame.grid()

    def hide(self):
        self.frame.grid_remove()