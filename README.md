# Tic Tac Royale
## Requirements
This project utilize Pyro4 for communication and in-memory storage. For client this project also utilize TkInter for user interface. Running this project requires you to use python module.

## Role
### Server 
Server will be used to process game logic and synchronization.

### Client
Client will be used to receive input from user.

## Running
### Server
Since this project utilize Pyro4 please run Pyro4 Name server using below command
`pyro4-ns --host=localhost --port=7777`
There are several server pre-setup to allow registering of all possible server to be used for fail recovery purpose. Please run below command to run it.
Alpha Server : `python -m server.runner.alpha`
Omega Server : `python -m server.runner.omega`
Epsilon Server : `python -m server.runner.epsilon`

### Client
Before running the client, please run atleast one server.
`python -m client.main`


