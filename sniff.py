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
import nodes
import config
import csv
import json
import networkx as nx

log.startLogging(sys.stdout)

hosts = nodes.Hosts()
#for t in config.cdc:
#    team = teams.Team(t["num"], config.getNetwork(t["num"]), t["name"])
#    ts.addTeam(team)

class SnifferService(TsharkService):
 
    def packetReceived(self, packet):
        """Override the TsharkService method"""
        try:
          sip = packet['ip'].src
          smac = packet['mac'].src
          dip = packet['ip'].dst
          dmac = packet['mac'].dst
          
          log.msg("src ip: %s dst ip: %s" % (sip, dip))
          if not hosts.get_host_by_mac(smac): 
            nodes.create_and_add_host(hosts, sip, smac)
          if not hosts.get_host_by_ip(sip):
            dnode = nodes.create_and_add_host(hosts, dip, dmac)
          dnode.add_packet(packet)
        except:
            pass

    def errReceived(self, data):
      print("errReceived! with %d bytes!" % len(data))

class Data(Resource):
    isLeaf = True
    def render_GET(self, request):
        stats = hosts.stats() 
        return json.dumps({ "nodes": stats[0], "links": stats[1]})

class Lines(Resource):
    isLeaf = True
    def render_GET(self, request):
        return json.dumps(config.line_ids)

class Nodes(Resource):
    isLeaf = True
    def render_GET(self, request):
        return json.dumps(config.node_ids)

class Graph(Resource):
    isLeaf = True
    G = nx.Graph()
    root = "Red Team"
    G.add_node(root)
    def render_GET(self, request):
        for team in ts.teams:
            G.add_node(team.name)
            G.add_edge(root, team.name)
            G[root][team.name]['weight'] = team.state.getAttackers()
        thresholds = [200, 400, 600, 800]

        low = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] < thresholds[0]]
        lowmed = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] in range(thresholds[0], thresholds[1])]
        med = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] in range(thresholds[1], thresholds[2])]
        himed = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] in range(thresholds[2], thresholds[3])]
        hi = [(u, v) for (u, v, d) in G.edges(data=True) if d['weight'] > thresholds[3]]
        a = 0.7

        pos = graphviz_layout(G, prog='twopi', args='')
        plt.figure(figsize=(8, 8))
        # nx.draw_networkx_nodes(G,pos,node_size=700)
        nx.draw_networkx_edges(G, pos, edgelist=low, width=1, alpha=a)
        nx.draw_networkx_edges(G, pos, edgelist=lowmed, width=2, alpha=a)
        nx.draw_networkx_edges(G, pos, edgelist=med, width=3, edge_color="red", alpha=a)
        nx.draw_networkx_edges(G, pos, edgelist=himed, width=4, edge_color="red", alpha=a)
        nx.draw_networkx_edges(G, pos, edgelist=hi, width=6, edge_color="red", alpha=a)
        # nx.draw_networkx_labels(G,pos,font_size=20,font_family='sans-serif')
        nx.draw(G, pos, node_size=180, alpha=0.5, node_color="blue", with_labels=True)
        plt.axis('equal')
        plt.savefig('graph.png')
        #plt.show()


def main():
    iface = sys.argv[1]
    print("listening on %s" % iface)
    root = static.File("./")
    root.putChild("data", Data())
#   root.putChild("lines", Lines())
#   root.putChild("nodes", Nodes())
    service = SnifferService([{"name" : iface, "filter": "port not 53 and not arp" }])
    reactor.listenTCP(80, server.Site(root))
    service.startService()
    reactor.run()


if __name__ == "__main__":
    main()
