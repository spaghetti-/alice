#!/usr/bin/python
from Alice import alice, util
import config

try:
    from twisted.internet import reactor
    from twisted.internet.task import LoopingCall
except ImportError:
    print "Error importing twisted libraries. Check if they are installed"
    exit(1)

if __name__ == '__main__':
    config = config.config
    lc = LoopingCall(util.streams.update)
    lc.start(300)
    reactor.connectTCP(config.getfqdn(config.host), config.port,
            alice.AliceFactory(config))
    reactor.run()
