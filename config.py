# config file

import socket

socket.setdefaulttimeout(20)

class Network(object):
    def __init__(self, nickname, alias, host, port, channel, linerate, CMDCHAR, authname, authpass):
        self.nickname = nickname
        self.alias = alias
        self.host = host
        self.port = port
        self.linerate = linerate
        self.channel = channel
        self.CMDCHAR = CMDCHAR
        self.authname = authname
        self.authpass = authpass

    def __repr__(self):
        return 'Network(%r, %r, %r, %r, %r, %r, %r)' % (self.nickname,
                self.alias, self.host, self.port, self.linerate, self.channel,
                self.CMDCHAR)

    def getfqdn(self, host):
        return socket.getfqdn(str(self.host))

def _createNetwork(nickname, alias, host, port, channel, linerate, CMDCHAR, authname):
    return Network(nickname, alias, host, port, channel, linerate, CMDCHAR, authpass)

# Set config here
nick = 'Alice'
#server = 'irc.freenode.net' #hostname @type str
server = 'irc.quakenet.org'
alias = 'quakenet' #casual name @type str
port = 6667 #port normally 6667 @type int
channel = "#samo.dota"
linerate = 10 #1 line per 10 seconds, in seconds @type int
CMDCHAR = '`' #@type char
authname = 'egrep' #for quacknet
authpass = '' #same
# end config

config = _createNetwork(nick, alias, server, port, channel, linerate, CMDCHAR, authname, authpass)
