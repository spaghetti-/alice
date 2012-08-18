# IRC bot based on twistedMatrix libraries
# @author potatoe

from twisted.internet import protocol
from Alice import alicecore

class AliceFactory(protocol.ClientFactory):

    protocol = alicecore.Alice

    def __init__(self, config):
        self.config = config
        self.nickname = self.config.nickname
        self.realname = self.config.nickname
        self.username = self.config.nickname
        self.versionName = 0
        self.linerate = self.config.linerate

    def clientConnectionFailed(self, connector, reason):
        print "Client connection failed: %s. Reconnecting.." % (reason)
        connector.connect()

    def clientConnectionLost(self, connector, reason):
        print "Client connection lost: %s. Reconnecting.." % (reason)
        connector.connect()
