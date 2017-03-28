import config
from twisted.python import log

class State(object):
    """There will be a current state for each team.  That state will
    contain information about the last X packets exchanged on that
    network according to what we care about.
    """
    def __init__(self, team_num):
        self.num_packets = 1000 # arbitrary, should be tweaked
        self.team_num = team_num
        # this is super inefficient.  But hey, it works!
        self.attackers = []
        self.defenders = []
        self.users = []

    def addPacket(self, packet):
        """We assume that if we got a packet here, its dest
        ip is in the team_num's ip space"""
        last_oct = int(packet['ip'].src.split(".")[3])
        log.msg("ip: %s LASTOCT: %s" % (packet['ip'].src, last_oct))
        if config.is_green(last_oct):
            self.addUser()
        elif config.is_red(last_oct):
            self.addAttack()
        else:
            self.addDefend()

    def addAttack(self):
        if len(self.attackers) > self.num_packets:
            self.popAll()
        self.attackers.append(True)
        self.defenders.append(False)
        self.users.append(False)

    def addUser(self):
        if len(self.attackers) > self.num_packets:
            self.popAll()
        self.attackers.append(False)
        self.defenders.append(False)
        self.users.append(True)

    def addDefend(self):
        if len(self.attackers) > self.num_packets:
            self.popAll()
        self.attackers.append(False)
        self.defenders.append(True)
        self.users.append(False)

    def popAll(self):
        self.attackers.pop(0)
        self.defenders.pop(0)
        self.users.pop(0)

    def getDefenders(self):
        count = 0
        for d in self.defenders:
            if d:
                count += 1
        return count

    def getAttackers(self):
        count = 0
        for a in self.attackers:
            if a:
                count += 1
        return count

    def getUsers(self):
        count = 0
        for u in self.users:
            if u:
                count += 1
        return count

    def getLen(self):
        return len(self.attackers)

    def getCounts(self):
        return self.getAttackers(), self.getUsers(), self.getDefenders()
