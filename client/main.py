import tkinter as tki
import client.frame.home as fHomeMod
import client.frame.create_room as fCreateRoomMod
import client.frame.join_room as fJoinRoomMod
import client.asset.font as fontMod
import client.frame.stack as stackMod
import client.client as clientMod
import client.frame.board_player as fBoardPlayer
import client.frame.watch_room as fWatchRoom
import client.client as clientMod
import typing as typ
import json

def RunGUI():
    root = tki.Tk()
    fontMod.Font.Initialize(root)
    root.title("Tic Tac Royale")
    root.resizable(width=False, height=False)
    servers = ["ALPHA-TicTacToeServer", "OMEGA-TicTacToeServer", "EPSILON-TicTacToeServer"]
    client = clientMod.TicTacToeClient("localhost", 7777, identifier="", servers=servers)
    stackFrame = stackMod.FrameStack(root)
    home = fHomeMod.Home(stackFrame, client)
    fCreateRoomMod.CreateRoom(stackFrame, client)
    fJoinRoomMod.JoinRoom(stackFrame, client)
    fBoardPlayer.BoardPlayer(stackFrame, client)
    fWatchRoom.WatchRoom(stackFrame, client)
    stackFrame.push(home)
    root.mainloop()

RunGUI()