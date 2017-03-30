from collections import OrderedDict

prefix = "10.10.20."
red_range = [10, 254]
green_range = [200, 228]

cdc = [
    {"num": 1, "name": "Dakota State"},
    {"num": 2, "name": "Governors State"},
    {"num": 3, "name": "Indiana Tech"},
    {"num": 4, "name": "Indiana University"},
    {"num": 5, "name": "Iowa State"},
    {"num": 6, "name": "John A Logan"},
    {"num": 7, "name": "Kansas State"},
    {"num": 8, "name": "Lewis"},
    {"num": 9, "name": "Southern Methodist"},
    {"num": 10, "name": "St. Johns"},
    {"num": 11, "name": "Central Florida"},
    {"num": 12, "name": "UIC"},
    {"num": 13, "name": "UIUC"},
    {"num": 14, "name": "Northern Iowa"},
    {"num": 15, "name": "Wright State"},
]

blue = {
    "File Server": "30",
    "Active Directory": "40",
    "HMI": "50",
    "Mail Server": "60",
    "Web Server": "70",
    "ESXi" : "2",
}

def getPrefix(team_num):
    return "10.0.%d0" % team_num

def getNetwork(team_num):
    return "%s.%s" % (getPrefix(team_num), "0")

def is_red(last_oct):
    if last_oct in range(red_range[0], red_range[1]):
        return True
    return False

def is_green(last_oct):
    if last_oct in range(green_range[0], green_range[1]):
        return True
    return False

# this is gettable from twisted while we're running
teamnets = []
for i in range(1, 16):
  teamnets.append(getNetwork(i))

line_ids = OrderedDict(

)

node_ids = OrderdDict(

)
