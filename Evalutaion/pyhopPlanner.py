from Helper import Hospital
import pyhop2
from math import sqrt

cleaningPowerHigh = 4
cleaningPowerLow = 1
timeLenght = 100
locations = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
robotConfig = ["Low", "Low", "High", "High"]
travelingWeightage = 0.2
########################################################################
# PyHop
domain_name = 'hospital_tasks'
pyhop2.Domain(domain_name)
rigid = pyhop2.State('rigid relations')


def getDistance(location1, location2):
    return sqrt((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2)


high = 0
low = 0
for robot in robotConfig:
    if robot == "High":
        high += 1
    else:
        low += 1


locationsForPyHop = locations + [[0, i] for i in range(len(robotConfig))]
locationsList = ['loc' + str(i + 1) for i in range(len(locations))] + ['botHome' + str(i + 1) for i in
                                                                       range(len(robotConfig))]
rigid.types = {
    'lowPower': ['robot' + str(i + 1) for i in range(low)],
    'highPower': ['robot' + str(low + i + 1) for i in range(high)],
    'location': locationsList}

distances = {}
for i in range(len(locationsList)):
    for j in range(len(locationsList)):
        if i < j:
            distances[(locationsList[i], locationsList[j])] = getDistance(locationsForPyHop[i], locationsForPyHop[j])

rigid.dist = distances

state0 = pyhop2.State()
stateLocation = {}
for i in range(len(robotConfig)):
    stateLocation['robot' + str(i + 1)] = 'botHome' + str(i + 1)

state0.loc = stateLocation
contaminations = {}
for i in range(len(locations)):
    contaminations[locationsList[i]] = 0

state0.contamination = contaminations
state0.display()

###################################################################
# Helper funcitons


lowPoweredRobots = []
highPoweredRobots = []


def seperateRobots(hopital, robots):
    global lowPoweredRobots
    global highPoweredRobots
    lowPoweredRobots = []
    highPoweredRobots = []
    for robot in robots:
        if hopital.robots[robot].power == "Low":
            lowPoweredRobots.append(robot)
        else:
            highPoweredRobots.append(robot)


def better_robot(robot, contamination):
    robotDistance = travel_cost(hospital.robots[robot].position, hospital.locations[contamination].position)
    busyRobots = hospital.getRobots("Busy")
    for i in busyRobots:
        if robotDistance - travel_cost(hospital.robots[i].position, hospital.locations[contamination].position) > 4:
            return True
        else:
            return False


def travel_cost(location1, location2):
    return sqrt((location1[0] - location2[0]) ** 2 + (location1[1] - location2[1]) ** 2) * travelingWeightage


def distance(x, y):
    return rigid.dist.get((x, y)) or rigid.dist.get((y, x))


def is_a(variable, type):
    return variable in rigid.types[type]


def choose_robot(state, contaminations, robots):
    indices = []

    for contamination in contaminations:
        seperateRobots(hospital, robots)
        if hospital.locations[contamination].status > 1:
            for robot in highPoweredRobots:
                if hospital.robots[robot].status == "Free":
                    if better_robot(robot, contamination):
                        break
                    else:
                        indices.append([robot, contamination])
                        robots.pop(robots.index(robot))
                        break
        else:
            for robot in lowPoweredRobots:
                if hospital.robots[robot].status == "Free":
                    indices.append([robot, contamination])
                    robots.pop(robots.index(robot))
                    break
    # for contamination in contaminations:
    #     distance = []
    #     for robot in robots:
    #         distance.append(getDistance(hospital.robots[robot].position, hospital.locations[contamination].position))
    #     if len(robots) > 0:
    #         indices.append([robots[distance.index(min(distance))], contamination])
    #         robots.pop(robots.index(robots[distance.index(min(distance))]))

    return indices


def send_robot(robot, location):
    rid = int(robot.replace('robot', '')) - 1
    lid = int(location.replace('loc', '')) - 1
    hospital.sendRobot(rid, lid)


##############################################
# Actions

def travel(state, r, x):
    if (is_a(r, 'lowPower') or is_a(r, 'highPower')) and is_a(x, 'location'):
        state.loc[r] = x
        # send_robot(r, x)
        return state


def clean(state, r, x):
    if is_a(r, 'lowPower') and is_a(x, 'location'):
        if state.loc[r] == x:
            state.contamination[x] -= cleaningPowerLow
            return state
    elif is_a(r, 'highPower') and is_a(x, 'location'):
        if state.loc[r] == x:
            state.contamination[x] -= cleaningPowerHigh
            return state


pyhop2.declare_actions(travel, clean)


##########################################
# Methods

def c_travel(state, r, x):
    if (is_a(r, 'lowPower') or is_a(r, 'highPower')) and is_a(x, 'location'):
        state.loc[r] = x
        send_robot(r, x)
        return state


def c_clean(state, r, x):
    if is_a(r, 'lowPower') and is_a(x, 'location'):
        if state.loc[r] == x:
            state.contamination[x] -= cleaningPowerLow
            return state
    elif is_a(r, 'highPower') and is_a(x, 'location'):
        if state.loc[r] == x:
            state.contamination[x] -= cleaningPowerHigh
            return state


pyhop2.declare_commands(c_travel, c_clean)


def do_nothing(state, contamination, robots):
    if len(contamination) == 0:
        return []


def clean_all(state, contamination, robots):
    actionsList = []
    if len(contamination) > 0:
        for i in contamination:
            state0.contamination['loc' + str(i + 1)] = hospital.locations[i].status
        indices = choose_robot(state, hospital.getContaminations(), hospital.getRobots("Free"))
        for index in indices:
            actionsList.append(('travel', 'robot' + str(index[0] + 1), 'loc' + str(index[1] + 1)))
            actionsList.append(('clean', 'robot' + str(index[0] + 1), 'loc' + str(index[1] + 1)))
        # print(actionsList)
        return actionsList


pyhop2.declare_task_methods('clean_hospital', do_nothing, clean_all)

pyhop2.set_current_domain(domain_name)
hospital = Hospital(locations, robotConfig)
# seperateRobots(hospital, hospital.robots)
for _ in range(timeLenght):
    hospital.tickOnce()
    print(hospital.getLocationsStatus(), hospital.cost)
    contaminations = hospital.getContaminations()
    pyhop2.find_plan(state0, [('clean_hospital', contaminations, hospital.robots)], verbose=0)
    pyhop2.run_lazy_lookahead(state0, [('clean_hospital', contaminations, hospital.robots)], verbose=0)

