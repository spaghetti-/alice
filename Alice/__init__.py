import re
import Alice.util as util

def isAdmin(user):
    admin = ['alice@kill.yourself.now.doitfaggot.org',
            'bob@bob-the-boss.users.quakenet.org', '~samo@41.233.108.71']
    for i in admin:
        if i.lower() == user.lower():
            return True
    return False

def parse_cmd(user, cmd):
    if cmd == 'streams':
        return util.streams.generateOut(util.streams.getlive())
    elif cmd.startswith('addstream') and isAdmin(user):
        return util.streams.addstream(util.urlgrab.grab(cmd)[0])
    elif cmd.startswith('delstream') and isAdmin(user):
        try:
            return util.streams.delstream(cmd.split(' ')[1])
        except:
            return 'Failed.'
    elif cmd.startswith('setalias') and isAdmin(user):
        try:
            return util.streams.setalias(cmd.split(' ')[1], cmd.split(' ')[2])
        except:
            return 'Failed'
    elif cmd == 'sync' and isAdmin(user):
        return util.streams.update()
    elif cmd == 'samo':
        return "smd"
    else:
        return "No such command or you lack privileges to use it."
