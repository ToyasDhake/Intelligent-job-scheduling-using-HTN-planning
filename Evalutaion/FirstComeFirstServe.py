from Helper import Hospital

timeLenght = 100

locations = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

robotConfig = ["Low", "Low", "High", "High"]
hospital = Hospital(locations, robotConfig)

robotConfigLength = len(robotConfig)
currentRobot = 0


def increaseCounter(val):
    val += 1
    val %= robotConfigLength
    return val


for _ in range(timeLenght):
    hospital.tickOnce()
    contaminations = hospital.getContaminations()
    for contamination in contaminations:
        freeRobots = hospital.getRobots("Free")
        while not currentRobot in freeRobots:
            currentRobot = increaseCounter(currentRobot)
        hospital.sendRobot(currentRobot, contamination)
        currentRobot = increaseCounter(currentRobot)
    print(hospital.getLocationsStatus(), hospital.cost)
