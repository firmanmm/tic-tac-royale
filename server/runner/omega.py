import server.app.tictactoeserver as tttServerMod

server = tttServerMod.TicTacToeServer("localhost", 7777, identifier="OMEGA-", syncServer=["ALPHA-TicTacToeServer", "EPSILON-TicTacToeServer"])
server.start()