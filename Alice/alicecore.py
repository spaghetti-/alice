from twisted.words.protocols import irc
from Alice import parse_cmd

class Alice(irc.IRCClient):

    def _get_nickname(self):
        return self.factory.nickname

    nickname = property(_get_nickname)
    #linerate = 10

    def signedOn(self):
        if self.factory.config.alias == 'quakenet':
            self.msg('Q@Cserve.quakenet.org', 'AUTH %s %s' % (self.factory.config.authname, self.factory.config.authpass))
            self.mode(self.nickname, '+', 'x')
            self.mode(self.nickname, '+', 'R')
        self.join(self.factory.config.channel)

    def joined(self, channel):
        print "Joined %s" % (channel)

    def privmsg(self, user, channel, msg):
        channel = channel.lower()
        lmsg = msg.lower().rstrip('\n\r')
        if channel.lower() == self.nickname.lower():
            self.msg(user, "I don't take private queries.")

        if lmsg.startswith(self.factory.config.CMDCHAR):
            cmd = lmsg[len(self.factory.config.CMDCHAR):]
            auser = user.split('!')[1]
            print auser, cmd
            self.say(channel, parse_cmd(auser, cmd))
