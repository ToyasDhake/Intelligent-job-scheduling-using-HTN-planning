from Helper import Hospital

timeLenght = 100

locations = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]

robotConfig = ["Low", "Low", "High", "High"]
hospital = Hospital(locations, robotConfig)

lowPoweredRobots = []
highPoweredRoobts = []

def seperateRobtos(hopital, robots):
    global lowPoweredRobots
    global highPoweredRoobts
    lowPoweredRobots = []
    highPoweredRoobts = []
    for robot in robots:
        if hopital.robots[robot].power == "Low":
            lowPoweredRobots.append(robot)
        else:
            highPoweredRoobts.append(robot)

for _ in range(timeLenght):
    hospital.tickOnce()
    contaminations = hospital.getContaminations()
    for contamination in contaminations:
        freeRobots = hospital.getRobots("Free")
        seperateRobtos(hospital, freeRobots)
        if hospital.locations[contamination].status > 1:
            for robot in highPoweredRoobts:
                if hospital.robots[robot].status == "Free":
                    hospital.sendRobot(robot, contamination)
                    break
        else:
            for robot in lowPoweredRobots:
                if hospital.robots[robot].status == "Free":
                    hospital.sendRobot(robot, contamination)
                    break

    print(hospital.getLocationsStatus(), hospital.cost)
