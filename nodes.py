class Host(object):
  """Class for a host or node.

  Attributes:
    connections (int)
    neighbors (dict like { host.id: weight})
    ip (string)
    mac (optional?, string)
    OS (optional, string)
  """
  def __init__(self, ip, mac):
    """initialize the object"""
    self.ip = ip
    self.mac = mac
    self.packets_seen = {}

  def add_neighbor(host, packet):
    """add a neighbor to neighbors
 
    Args:
      host (host object) 
    """
    if not self.neighbors:
      self.neighbors = {}
    self.increment_neighbor(host.get_id())
    self.add_packet(packet)

  def increment_neighbor(host_id):
    """increments the weight of the given neighbor"""
    self.neighbors[host_id] += 1
    
  def decrement_neighbor(host_id):
    """decrements the weight of the given neighbor"""
    if self.neighbors[host_id]:
      self.neighbors[host_id] -= 1

  def get_mac(self):
    """getter for mac address"""
    return self.mac

  def get_ip(self):
    """getter for ip address"""
    return self.ip
  
  def get_neighbors(self):
    """getter for neighbors"""
    return self.neighbors
  
  def get_neighbor_ids(self):
    """returns a list of neighbor ids (int)"""
    return [self.hosts.index(h) for h in hosts]

  def add_host_id(self, idx):
    """should only be run once, when host is created and added to hosts"""
    self.id = idx

  def add_packet(self, packet, time):
    """add a packet to seen for time x...

    packets will queue up for a given time so that you can clear them out
    later, so time should be a minute or second value, not a timestamp.
    """
    if time not in self.packets:
      self.packets[time] = [packet]
    else:
      self.packets[time].append(packet)
  

class Hosts(object):
  """Class for a group of hosts"""

  def __init__(self):
    self.hosts = []

  def get_host_id(self, host):
    """get the id for a host"""
    return self.hosts.index(host)

  def add_host(self, host):
    """add a host
 
    Args:
      host (host object)
    
    Returns:
      host id (list index)
    """
    self.hosts.append(host)
    idx = get_host_id(host)
    host.add_id(idx)
    return idx

  def get_host_by_id(self, id):
    """gets a host by id. this is O(1)
   
    Args: 
      id (int)
  
    Returns:
      host object for given id
    """
    return self.hosts[id]

  def get_host_by_mac(self, mac):
    """gets a host by mac. this is O(n)

    Args:
      mac (string)
  
    Returns:
      host object for given mac, False if not found
    """
    for h in self.hosts:
      if h.get_mac() == mac:
       return h
    return False

  def get_host_by_ip(self, ip):
    """gets a host by ip. this is O(n)

    Args:
      ip (string)
 
    Returns:
      host object for given ip
    """
    for h in self.hosts:
      if h.get_ip() == ip:
        return h
    return False

  def stats(self):
    nodes = []
    links = []
    for idx, host in enumerate(self.hosts):
      nodes.append({
        "ip": host.get_ip(),
        "mac": host.get_mac(),
        "group": 1, # this is for coloring
      })
      for nid, weight  in host.get_neighbors().items():
        links.append({
          "source": idx,
          "target": nid,
          "value": weight
        })
    #TODO: links = dedup_links(links)
    return nodes, links

def create_and_add_host(hosts, ip, mac):
  new_host = Host(ip, mac)
  idx = hosts.add_host(new_host)
  new_host.add_id(idx)
  return new_host
