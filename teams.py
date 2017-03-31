import state
from twisted.python import log

class Team(object):
    def __init__(self, num, network, name):
        self.num = num
        self.network = network
        self.name = name # this will be the school for us
        self.state = state.State(self.num)

    def contains(self, ip):
        netocts = self.network.split(".")
        ipocts = ip.split(".")
        if (netocts[0] == ipocts[0] and netocts[2] == ipocts[2]):
            return True
        return False

    #self.seen_ips = []

class Teams(object):
    def __init__(self):
        self.teams = []

    def addTeam(self, team):
        self.teams.append(team)

    def getTeam(self, num):
        return self.teams[num-1]

    def slotPacket(self, packet):
        for team in self.teams:
            #log.msg("type: %s contains: %s" % (type(packet["ip"].dst), packet["ip"].dst))
            try:
                if team.contains(packet["ip"].dst):
                    team.state.addPacket(packet)
                    return True

            except:
                pass

    def dump(self):
        l = []
        for team in self.teams:
            attacker, user, defender, fileattack, adattack, \
            hmiattack, mailattack, webattack, esxi = team.state.getCounts()
            l.append({
              "num" : team.num,
              "name": team.name,
              "network": team.network,
              "attacker" : attacker,
              "user" : user,
              "defender": defender,
              "fileattack": fileattack,
              "adattack" : adattack,
              "hmiattack" : hmiattack,
              "mailattack" : mailattack,
              "webattack" : webattack,
              "esxi": esxi
            })
        return l
