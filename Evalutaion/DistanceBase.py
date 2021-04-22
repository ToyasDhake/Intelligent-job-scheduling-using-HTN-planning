from Helper import Hospital
from math import sqrt
timeLenght = 100

locations = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

def getDistance(robot, location):
    return sqrt((robot[0]-location[0])**2+(robot[1]-location[1])**2)

hospital = Hospital(locations,  ["Low", "Low", "High"])
for _ in range(timeLenght):
    contaminations = hospital.getContaminations()
    if len(contaminations) > 0:
        freeRobots = hospital.getRobots("Free")
        distance = []
        for robot in freeRobots:
            distance.append(getDistance(hospital.robots[robot].position, hospital.locations[contaminations[0]].position))
        if len(freeRobots)>0:
            hospital.sendRobot(freeRobots[distance.index(min(distance))], contaminations[0])

    hospital.tickOnce()
    print(hospital.getLocationsStatus(), hospital.cost)
