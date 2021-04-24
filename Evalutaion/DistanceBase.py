from Helper import Hospital
from math import sqrt

timeLenght = 100

locations = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
robotConfig = ["Low", "Low", "High", "High"]


def getDistance(robot, location):
    return sqrt((robot[0] - location[0]) ** 2 + (robot[1] - location[1]) ** 2)


hospital = Hospital(locations, robotConfig)
for _ in range(timeLenght):
    hospital.tickOnce()
    contaminations = hospital.getContaminations()
    for contamination in contaminations:
        freeRobots = hospital.getRobots("Free")
        distance = []
        for robot in freeRobots:
            distance.append(getDistance(hospital.robots[robot].position, hospital.locations[contamination].position))
        if len(freeRobots) > 0:
            hospital.sendRobot(freeRobots[distance.index(min(distance))], contamination)

    print(hospital.getLocationsStatus(), hospital.cost)
