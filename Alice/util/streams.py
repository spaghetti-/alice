# Streams class, rewritten with JSON because fuck XML
# Utilities for managing twitch.tv and own3d.tv streams
# @author potatoe

import sqlite3 as sqlite, simplejson as json, unicodedata, re
import urlgrab, urllib
from urlparse import urlparse

class Streams(object):
    def __init__(self, db, table):
        self.db = db
        self.con = sqlite.connect(db)
        self.cur = self.con.cursor()
        self.table = table

    def __repr__(self):
        return 'Streams(%r, %r)' % (self.db, self.table)

    def _sanitize(self, string):
        string = string.replace('"', '')
        if isinstance(string, unicode):
            return unicodedata.normalize('NFKD', string).encode('ASCII', 'ignore')
        return string

    def _dbcmd(self, cmd):
        self.cur.execute(cmd)
        _row = self.cur.fetchall()
        self.con.commit()
        return _row

    def count(self):
        cmd = 'SELECT * FROM %s' % (self.table)
        return 'I have %d streams in my list.' % int((len(self._dbcmd(cmd))))

    def addstream(self, url):
        _url = urlparse(url)
        _details = self._check(_url.path, _url.hostname)
        if not _details:
            return "Invalid id."
        if(self._exists(_details[1])):
            return "Entry exists"
        cmd = 'INSERT INTO %s(login, id, server) VALUES("%s", "%r", "%s")' % (self.table, _details[1], int(_details[0]), _details[2])
        self._dbcmd(cmd)
        return self.count()

    def _check(self, path, server):
        server = server.split('.')[len(server.split('.')) - 2]
        if server == 'own3d':
            APICALL = 'http://api.own3d.tv/rest/user/show.json?id=%s' % (re.findall('\d+', path)[0])
            _jsondata = json.loads(urllib.urlopen(APICALL).read())
            if _jsondata:
                return _jsondata['id'], _jsondata['name'], server
            else:
                return False
        if server == 'twitch':
            APICALL = 'http://api.justin.tv/api/channel/show/%s.json' % (path)
            _jsondata = json.loads(urllib.urlopen(APICALL).read())
            try:
                return _jsondata['id'], _jsondata['login'], server
            except:
                return False

    def _exists(self, login):
        cmd = 'SELECT * FROM %s WHERE login="%s"' % (self.table, login)
        row = self._dbcmd(cmd)
        if row:
            return True
        if not row:
            return False
        return False

    def _updatetwitch(self, slist):
        APICALL = "http://api.justin.tv/api/stream/list.json?channel=%s" % (slist)
        _jsondata = json.loads(urllib.urlopen(APICALL).read())
        for livefag in _jsondata:
            login = livefag['channel']['login']
            viewers = livefag['channel_count']
            cmd = 'UPDATE %s SET live="1", viewers="%d" WHERE login="%s"' % (self.table, viewers, login)
            self._dbcmd(cmd)

    def _updateown3d(self, uid):
        APICALL = 'http://api.own3d.tv/rest/live/status.json?liveid=%s' % (uid)
        _jsondata = json.loads(urllib.urlopen(APICALL).read())
        try:
            islive = int(_jsondata['live_is_live'])
            if islive == 1:
                viewers = _jsondata['live_viewers']
                cmd = 'UPDATE %s SET live="1", viewers="%d" WHERE id="%d"' % (self.table, int(viewers), int(uid))
                self._dbcmd(cmd)
            else:
                pass
        except:
            pass

    def _normalize(self):
        cmd = 'UPDATE %s SET live=0, viewers=0' % (self.table)
        self._dbcmd(cmd)

    def update(self):
        self._normalize()
        cmd = 'SELECT * FROM %s WHERE server="twitch"' % (self.table) #twitch first
        rows = self._dbcmd(cmd)
        slist = ''
        for row in rows:
            slist += row[0]
            slist += ','
        slist = slist[:-1]
        self._updatetwitch(slist)
        cmd = 'SELECT * FROM %s WHERE server="own3d"' % (self.table)
        rows = self._dbcmd(cmd)
        for row in rows:
            #can't update own3d streams together in one query
            self._updateown3d(row[1])
        print "Updated via looping call"
        return "Database updated."

    def getlive(self):
        cmd = 'SELECT * FROM %s WHERE live=1 ORDER BY viewers DESC' % (self.table)
        rows = self._dbcmd(cmd)
        results = []
        for row in rows:
            if row[2] == 'twitch':
                results.append((row[0], row[4], row[6], 'twitch'))
            if row[2] == 'own3d':
                results.append((row[1], row[4], row[6], 'own3d'))
        return results

    def generateOut(self, results):
        out = ''
        for i in results:
            if i[3] == 'twitch':
                _s = '\x0312www.twitch.tv/%s\x03 (%s) ' % (i[0], i[1])
                out += _s
            if i[3] == 'own3d':
                if i[2]:
                    _s = '\x0312www.own3d.tv/live/%s\x03 %s (%s) ' % (i[0], i[2], i[1])
                    out += _s
                else:
                    _s = '\x0312www.own3d.tv/live/%s\x03 (%s) ' % (i[0], i[1])
                    out += _s
        return self._sanitize(out)

    def setalias(self, uid, alias):
        cmd = 'UPDATE %s SET hname="%s" WHERE id="%s"' % (self.table, alias, str(uid))
        self._dbcmd(cmd)
        return "Alias set if id exists."

    def delstream(self, identifier):
        cmd = 'DELETE FROM %s WHERE id="%s" OR login="%s"' % (self.table, identifier, identifier)
        self._dbcmd(cmd)
        return "Deleted if existed."

streams = Streams('streams.db', 'dotastreams')
