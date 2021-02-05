class Column:
    def __init__(self, _id, _status, _amountOfFloors, _amountOfElevators):
        self.ID = _id
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.amountOfElevators = _amountOfElevators
        self.elevatorsList = []
        self.callButtonsList = []

        self.createElevators(_amountOfFloors, _amountOfElevators)
        self.createCallButtons(_amountOfFloors)

    def display(self):
        print("Column: " + str(self.ID))
        print("Floors: " + str(self.amountOfFloors))
        print("Elevators: " + str(self.amountOfElevators))

    def createCallButtons(self, _amountOfFloors):
        buttonID = 1

        for i in range(1, self.amountOfFloors):
            if i < self.amountOfFloors:
                callButton = CallButton(1, 'off', i, 'up')
                self.callButtonsList.append(CallButton)
                buttonID += 1

            if i >= 2:
                callButton = CallButton(
                    2, 'off', i, 'down')
                self.callButtonsList.append(CallButton)
                buttonID += 1

    def createElevators(self, _amountOfFloors, _amountOfElevators):
        for i in range(self.amountOfElevators):
            elevator = Elevator(i + 1, 'idle', _amountOfFloors, 1)
            self.elevatorsList.append(elevator)

    def requestElevator(self, _floor, _direction):
        print("||-PASSENGER REQUESTS PICKUP AT FLOOR " +
              str(_floor) + " TO GO " + str(_direction) + "-||")
        elevator = self.findElevator(_floor, _direction)
        elevator.floorRequestList.append(_floor)
        elevator.sortFloorList()
        print()
        print("ELEVATOR " + str(elevator.ID) + " MOVES FROM FLOOR " +
              str(elevator.currentFloor) + " TO GO TO FLOOR " + str(_floor))
        elevator.move()
        return elevator

    # We use a score system depending on the current elevators state. Since the bestScore and the referenceGap are
    # higher values than what could be possibly calculated, the first elevator will always become the default bestElevator,
    # before being compared with to other elevators. If two elevators get the same score, the nearest one is prioritized.

    def findElevator(self, requestedFloor, requestedDirection):
        bestElevatorInformations = {
            "bestElevator": None,
            "bestScore": 5,
            "referenceGap": 10000000
        }

        for elevator in self.elevatorsList:
            # The elevator is at my floor and going in the direction I want
            if requestedFloor == elevator.currentFloor and elevator.status == 'stopped' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(
                    1, elevator, bestElevatorInformations, requestedFloor)

            # The elevator is lower than me, is coming up and I want to go up
            elif requestedFloor > elevator.currentFloor and elevator.direction == 'up' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(
                    2, elevator, bestElevatorInformations, requestedFloor)

            # The elevator is higher than me, is coming down and I want to go down
            elif requestedFloor < elevator.currentFloor and elevator.direction == 'down' and requestedDirection == elevator.direction:
                bestElevatorInformations = self.checkIfElevatorIsBetter(
                    2, elevator, bestElevatorInformations, requestedFloor)

            # The elevator is idle
            elif elevator.status == 'idle':
                bestElevatorInformations = self.checkIfElevatorIsBetter(
                    3, elevator, bestElevatorInformations, requestedFloor)

            # The elevator is not available, but still could take the call nothing else better is found
            else:
                bestElevatorInformations = self.checkIfElevatorIsBetter(
                    4, elevator, bestElevatorInformations, requestedFloor)

            #bestElevator = bestElevatorInformations["bestElevator"]
            #bestScore = bestElevatorInformations["bestScore"]
            #referenceGap = bestElevatorInformations["referenceGap"]
        print()
        print(">>[ELEVATOR TO BE SENT]:")
        print(bestElevatorInformations["bestElevator"])
        return bestElevatorInformations["bestElevator"]

    def checkIfElevatorIsBetter(self, scoreToCheck, newElevator, bestElevatorInformations, floor):
        if scoreToCheck < bestElevatorInformations["bestScore"]:
            bestElevatorInformations["bestScore"] = scoreToCheck
            bestElevatorInformations["bestElevator"] = newElevator
            bestElevatorInformations["referenceGap"] = abs(
                newElevator.currentFloor - floor)
        elif bestElevatorInformations["bestScore"] == scoreToCheck:
            gap = abs(newElevator.currentFloor - floor)
            if (bestElevatorInformations["referenceGap"] > gap):
                bestElevatorInformations["bestScore"] = scoreToCheck
                bestElevatorInformations["bestElevator"] = newElevator
                bestElevatorInformations["referenceGap"] = gap
        return bestElevatorInformations


class Elevator:
    def __init__(self, _id, _status, _amountOfFloors, _currentFloor):
        self.ID = _id
        self.status = _status
        self.amountOfFloors = _amountOfFloors
        self.currentFloor = _currentFloor
        self.direction = None
        self.door = Door(_id, 'closed')
        self.floorRequestButtonsList = []
        self.floorRequestList = []

        self.createFloorRequestButtons(_amountOfFloors)

    def createFloorRequestButtons(self, _amountOfFloors):
        buttonFloor = 1
        for i in range(0, _amountOfFloors):
            floorRequestButton = FloorRequestButton(
                1, 'off', buttonFloor)
            self.floorRequestButtonsList.append(floorRequestButton)
            buttonFloor += 1
            floorRequestButton.ID += 1

    # Simulate when a user press a button inside the elevator//
    def requestFloor(self, _floor):
        print()
        print("||-PASSENGER NOW INSIDE ELEVATOR REQUESTS TO GO TO FLOOR " +
              str(_floor) + "-||")
        self.floorRequestList.append(_floor)
        self.sortFloorList()
        print()
        print("ELEVATOR " + str(self.ID) + " MOVES FROM FLOOR " +
              str(self.currentFloor) + " TO GO TO FLOOR " + str(_floor))
        self.move()

    def move(self):
        while len(self.floorRequestList) != 0:
            destination = self.floorRequestList[0]
            self.status = 'moving'
            if self.currentFloor < destination:
                self.direction = 'up'
                while self.currentFloor < destination:
                    self.currentFloor += 1

            elif self.currentFloor > destination:
                self.direction = 'down'
                while self.currentFloor > destination:
                    self.currentFloor -= 1

            self.status = 'stopped'
            self.floorRequestList.pop()

        if len(self.floorRequestList) == 0:
            self.status = 'idle'

    def sortFloorList(self):
        if self.direction == 'up':
            sorted(self.floorRequestList)
        else:
            sorted(self.floorRequestList, reverse=True)


class CallButton:
    def __init__(self, _id, _status, _floor, _direction):
        self.ID = _id
        self.status = _status
        self.floor = _floor
        self.direction = _direction


class FloorRequestButton:
    def __init__(self, _id, _status, _floor):
        self.ID = _id
        self.status = _status
        self.floor = _floor


class Door:
    def __init__(self, _id, _status):
        self.ID = _id
        self.status = _status


# SCENARIO TERMINAL SIMULATIONS

# -----INSTRUCTIONS-----#

# TO SIMULATE A SCENARIO IN THE TERMINAL, SIMPLY UNCOMMENT (REMOVE THE #) THE DESIRED FUNCTION AT THE BOTTOM OF THE FILE (EXAMPLE: scenario1())

# ___________________________________________________________________________________________________________________________________________#


# ----------------------SCENARIO 1---------------------//

# Elevator 1 is Idle at floor 2
# Elevator 2 is Idle at floor 6
# Someone is on floor 3 and wants to go to the 7th floor.
# Elevator 1 is expected to be sent.

def scenario1():
    print()
    print("______________________________________________________________________________________________")
    print()
    print("--------------------SCENARIO #1--------------------")
    column = Column(1, 'online', 10, 2)
    column.display()
    column.elevatorsList[0].currentFloor = 2
    column.elevatorsList[1].currentFloor = 6
    print()
    elevator = column.requestElevator(3, 'up')
    elevator.requestFloor(7)
    print()
    print("______________________________________________________________________________________________")
    print()


# ----------------------SCENARIO 2---------------------//

# Elevator 1 is Idle at floor 10
# Elevator 2 is idle at floor 3
# Someone is on the 1st floor and requests the 6th floor.
# Elevator 2 should be sent.
# 2 minutes later, someone else is on the 3rd floor and requests the 5th floor. Elevator 2 should be sent.
# Finally, a third person is at floor 9 and wants to go down to the 2nd floor.
# Elevator 1 should be sent.

def scenario2():
    print()
    print("______________________________________________________________________________________________")
    print()
    print("--------------------SCENARIO #2--------------------")
    column = Column(1, 'online', 10, 2)
    column.display()
    column.elevatorsList[0].currentFloor = 10
    column.elevatorsList[1].currentFloor = 3
    print()
    print("-----[REQUEST #1]-----")
    print()
    elevator = column.requestElevator(1, 'up')
    elevator.requestFloor(6)
    print()
    print()
    print("-----[REQUEST #2]-----")
    print()
    print()
    column.elevatorsList[1].currentFloor = 6
    elevator = column.requestElevator(3, 'up')
    elevator.requestFloor(5)
    print()
    print()
    print("-----[REQUEST #3]-----")
    print()
    print()
    elevator = column.requestElevator(9, 'down')
    elevator.requestFloor(2)
    print()
    print("______________________________________________________________________________________________")
    print()


# ----------------------SCENARIO 3---------------------//

# Elevator A is Idle at floor 10
# Elevator B is Moving from floor 3 to floor 6
# Someone is on floor 3 and requests the 2nd floor.
# Elevator A should be sent.
# 5 minutes later, someone else is on the 10th floor and wants to go to the 3rd. Elevator B should be sent.

def scenario3():
    print()
    print("______________________________________________________________________________________________")
    print()
    print("--------------------SCENARIO #3--------------------")
    column = Column(1, 'online', 10, 2)
    column.display()
    column.elevatorsList[0].currentFloor = 10
    column.elevatorsList[1].currentFloor = 3
    column.elevatorsList[1].status = 'moving'
    print()
    print("-----[REQUEST #1]-----")
    print()
    elevator = column.requestElevator(3, 'down')
    elevator.requestFloor(2)
    print()
    print("-----[REQUEST #2]-----")
    print()
    column.elevatorsList[1].currentFloor = 6
    column.elevatorsList[1].status = 'idle'
    elevator = column.requestElevator(10, 'down')
    elevator.requestFloor(3)
    print()
    print("______________________________________________________________________________________________")
    print()

# TO SIMULATE A SCENARIO IN THE TERMINAL, SIMPLY UNCOMMENT (REMOVE THE #) THE DESIRED FUNCTION


# scenario1()
# scenario2()
# scenario3()
