import Pyro4
import json
import base64


class Server:
    def __init__(self, host, port, identifier="main-"):
        self.host = host
        self.port = port
        self.identifier = identifier

    def Start(self, objects):
        daemon = Pyro4.Daemon(self.host)
        ns = Pyro4.locateNS(self.host, self.port)
        for obj in objects:
            Pyro4.expose(obj.__class__)
            objAddress = daemon.register(obj)
            ns.register("%s%s" % (self.identifier, type(obj).__name__), objAddress)
        daemon.requestLoop()