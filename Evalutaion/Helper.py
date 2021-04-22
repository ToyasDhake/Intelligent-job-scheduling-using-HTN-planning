from numpy.random import rand, randint
from math import sqrt

cleaningPowerHigh = 2
cleaningPowerLow = 0.5

travelingWeightage = 0.2


class Robot:
    def __init__(self, power, position, status="Free"):
        self.power = power
        self.position = position
        self.status = status


class Location:
    def __init__(self, position, status=0, isFree=True):
        self.position = position
        self.status = status
        self.isFree = isFree


class Hospital:
    def __init__(self, locations, robots, contaminationRate=0.25):
        self.locations = [Location(position) for position in locations]
        self.robots = [Robot(robot, [0, i]) for i, robot in enumerate(robots)]
        self.contaminationRate = contaminationRate
        self.time = 0
        self.cost = 0

    def getContaminations(self):
        result = []
        for loction in self.locations:
            if loction.status != 0 and loction.isFree:
                result.append(self.locations.index(loction))
        return result

    def getRobots(self, code):
        result = []
        for robot in self.robots:
            if robot.status == code:
                result.append(self.robots.index(robot))
        return result

    def getLocationsStatus(self):
        return [location.status for location in self.locations]

    def sendRobot(self, robotID, locationID):
        if self.locations[locationID].isFree:
            self.cost += sqrt((self.robots[robotID].position[0] - self.locations[locationID].position[0]) ** 2 + (
                        self.robots[robotID].position[1] - self.locations[locationID].position[1]) ** 2)
            self.robots[robotID].position = self.locations[locationID].position
            if self.locations[locationID].status != 0:
                self.robots[robotID].status = "Busy"
            self.locations[locationID].isFree = False
            return True
        else:
            return False

    def tickOnce(self):
        self.time += 1
        if rand() < self.contaminationRate:
            temp = True
            while temp:
                val = randint(0, len(self.locations))
                if self.locations[val].status == 0:
                    self.locations[val].status = randint(1, 3)
                    temp = False
        for location in self.locations:
            self.cost += location.status

        busyRobots = self.getRobots("Busy")

        for robot in busyRobots:
            for i in range(len(self.locations)):
                if self.robots[robot].position == self.locations[i].position:
                    if self.locations[i].status != 0:
                        if self.robots[robot].power == "High":
                            self.locations[i].status -= cleaningPowerHigh
                        else:
                            self.locations[i].status -= cleaningPowerLow
                        if self.locations[i].status < 0:
                            self.locations[i].status = 0
                    else:
                        self.robots[robot].status = "Free"
                        self.locations[i].isFree = True


if __name__ == "__main__":
    locations = [[1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [7, 7], [8, 8], [9, 9]]
    hospital = Hospital(locations, ["Low", "Low", "High"])
    for _ in range(10):
        hospital.tickOnce()
