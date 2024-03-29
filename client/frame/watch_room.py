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
import threading
import time
import enum
import sys
import random

class WatchRoom(baseMod.IBase):

    def __init__(self, stackFrame: stackMod.FrameStack, client: clientMod.TicTacToeClient):
        self.allowedColorChar = "0123456789ABCDEF"
        self.roomCodeToColor : typ.Dict[int, str] = dict()
        self.roomColorToCode : typ.Dict[str, int] = dict()
        self.historyOffset = 0
        self.lock = threading.Lock()
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
            text="Watching",
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
                btnGrid = tki.Button(btnFrame, text=" ", font=fontMod.Font.PawnGridFont, background="white")
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
                exit()
        except Exception as e:
            traceback.print_exc()
            msgMod.showerror("Error", str(e))
        print("Clicked : X : %d, Y : %d" % (x, y))
        self.synchronize()


    def updateGrid(self):
        print("Updating Grid Display")
        for i in range(11):
            for j in range(11):
                grid = self.board[i][j]
                symbol = " "
                xPos = j - 5 + self.xLocation.get()
                yPos = -i + 5 + self.yLocation.get()
                pawn = self.client.getPawnAtCoordinate(xPos, yPos)
                background = "white"
                if pawn is not None:
                    loc = pawn.getLocation()
                    symbol = pawn.getPawnSymbol()
                    background = self.getColor(pawn.getRoomCode())
                grid.configure(text=symbol, background=background)

    def updateHistory(self):
        try:
            history = self.client.getPlacement()
            upper = len(history) - self.historyOffset
            if upper < 0:
                upper = 0
            elif upper >= len(history):
                upper = len(history)
            lower = upper - 10
            if lower < 0:
                lower = 0
            elif lower >= len(history):
                lower = len(history)
            print("Lower %d, Upper %d" % (lower, upper))
            if upper <= lower:
                history = list()
            else:
                history = history[lower : upper]
            for i in range(10):
                historyTab = self.histories[i]
                newTxt = ""
                idx = 9 - i
                background = "#FFFFFF"
                if idx >= 0 and idx < len(history):
                    data = history[idx]
                    location = data.getLocation()
                    newTxt = "Room %d placed %s at (%d, %d)" % (data.getRoomCode(), data.getPawnSymbol(), location.getX(), location.getY())
                    background = self.getColor(data.getRoomCode())
                historyTab.configure(text=newTxt, background=background)
        except Exception as e:
            print(str(e))

    def getColor(self, roomCode: int) -> str:
        if roomCode in self.roomCodeToColor:
            return self.roomCodeToColor[roomCode]
        color = self.generateColor()
        while color in self.roomColorToCode:
            color = self.generateColor()
        self.roomCodeToColor[roomCode] = color
        self.roomColorToCode[color] = roomCode
        return color

    def generateColor(self) -> str:
        color = "#"
        for i in range(6):
            randIdx = random.randint(0, len(self.allowedColorChar) - 1)
            color = "%s%s" % (color, self.allowedColorChar[randIdx])
        return color

    def upHistory(self):
        self.historyOffset += 1
        history = self.client.getPlacement()
        if self.historyOffset >= len(history):
            self.historyOffset = len(history) - 1
        self.synchronize()

    def downHistory(self):
        self.historyOffset -= 1
        if self.historyOffset < 0:
            self.historyOffset = 0
        self.synchronize()

    def changeCenter(self):
        print("Center Changed To X : %d and Y : %d" % (self.xLocation.get(), self.yLocation.get()))
        self.synchronize()

    def show(self):
        self.frame.grid()
        thread = threading.Thread(target=self.synchronizeRoutine, daemon=True)
        thread.start()

    def hide(self):
        self.frame.grid_remove()

    def synchronizeRoutine(self):
        while True:
            try:
                self.synchronize()
                time.sleep(2)
            except KeyboardInterrupt as e:
                print("Keyboard Interrupt")
                sys.exit(1)
                break
            except Exception as e:
                pass

    def synchronize(self):
        self.lock.acquire(timeout=2)
        try:
            self.client.synchronize()
            self.updateHistory()
            self.updateGrid()
        except Exception as e:
            print(str(e))
            self.lock.release()
        self.lock.release()