import server.app.tictactoeserver as tttServerMod

server = tttServerMod.TicTacToeServer("localhost", 7777, identifier="EPSILON-", syncServer=["ALPHA-TicTacToeServer", "OMEGA-TicTacToeServer"])
server.start()