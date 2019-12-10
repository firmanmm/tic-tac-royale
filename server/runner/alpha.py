import server.app.tictactoeserver as tttServerMod

server = tttServerMod.TicTacToeServer("localhost", 7777, identifier="ALPHA-", syncServer=["OMEGA-TicTacToeServer", "EPSILON-TicTacToeServer"])
server.start()