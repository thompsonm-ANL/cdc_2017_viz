from __future__ import print_function

"""
requires: python-twisted txshark
"""
import sys
from twisted.python import log
from txshark import TsharkService
from twisted.internet import reactor
from twisted.web.resource import Resource
from twisted.web import static, server, twcgi
import teams
import config
import csv
import json

log.startLogging(sys.stdout)

num_teams = 15

ts = teams.Teams()
for i in range(1, num_teams+1):
    team = teams.Team(i, config.getNetwork(i), "team %d" % i)
    ts.addTeam(team)

class SnifferService(TsharkService):
    def packetReceived(self, packet):
        """Override the TsharkService method"""
        #log.msg("Packet received: {}".format(packet))
        ts.slotPacket(packet)
        # with open (filename, "wb") as f:
        #     wr = csv.writer(f, quoting=csv.QUOTE_MINIMAL)
        #     wr.writerow(["num", "name", "network", "attacker", "user", "defender"])
        #     for t in ts.teams:
        #         l = []
        #         l.append(t.num)
        #         l.append(t.name)
        #         l.append(t.network)
        #         l.extend(t.state.getCounts())
        #         wr.writerow(l)

class Data(Resource):
    isLeaf = True
    def render_GET(self, request):
        return json.dumps(ts.dump())

def main():
    iface = sys.argv[1]
    print("listening on %s" % iface)
    root = static.File("./")
    root.putChild("data", Data())
    service = SnifferService([{"name" : iface, "filter": "dst net 10.0.0.0/8"}])
    reactor.listenTCP(80, server.Site(root))
    service.startService()
    reactor.run()


if __name__ == "__main__":
    main()
