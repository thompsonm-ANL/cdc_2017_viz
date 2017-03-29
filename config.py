prefix = "10.10.20."
red_range = [1, 50]
green_range = [100, 250]

def getNetwork(team_num):
    return "10.0.%d0.0" % team_num

def is_red(last_oct):
    if last_oct in range(red_range[0], red_range[1]):
        return True
    return False

def is_green(last_oct):
    if last_oct in range(green_range[0], green_range[1]):
        return True
    return False
