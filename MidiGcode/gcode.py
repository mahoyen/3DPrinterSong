# Constants
FREQUENCYTOFEEDRATECONSTANT = 1
TIMETODISTANCECONSTANT = 1
BUILDING_AREA = [223, 223, 305] # [X, Y, Z]
EPSILON = [10, 10, 10] # [X, Y, Z]
STARTPOSITION = [100, 100, 100] # [X, Y, Z]

# Global variables
direction = [1,1,1] # [X, Y, Z]

# Converts frequency and time into feedrate and distance
def getFeedrateDistanceMatrix(frequencyTimeMatrix):
    return [[float(FREQUENCYTOFEEDRATECONSTANT*f), float(FREQUENCYTOFEEDRATECONSTANT*TIMETODISTANCECONSTANT*f/T)] for f, T in frequencyTimeMatrix]

# Converts distances to coordinates. returns list[list[list[x, y, z], feedrate]]
def translateFrequencyTimeMatrixToCoordinates(frequencyTimeMatrix):
    coordinateList = {}
    for frequencies, duration in frequencyTimeMatrix:
        sumFeedrate = 0
        feedrates = list()
        for i in range(len(freqncies)):
            feedrates[i] = FREQUENCYTOFEEDRATECONSTANT * freq
            sumFeedrate += feedrate**2
        absoluteFeedrate = sumFeedrate**0.5
        coordinateList.append([[feedrate*duration for feedrate in feedrates], absoluteFeedrate])
    
    return coordinateList
    # return [[relX, 0, 0] for feedrate, relX in feedrateDistanceMatrix]

# Returns relative coordinate-vector from distance
# def translateDistanceToCoordinate(distance):
#     return [distance, 0, 0]

# Returns true if all notes in noteList are zero
def isSilent(noteList):
    for i in noteList:
        if i:
            return False
    return True

# Returns True if coordinate is outside build area
def isCoordinateOutside(coordinate):
    for i in range(len(coordinate)):
        if coordinate[i] < EPSILON[i] or coordinate[i] > BUILDING_AREA[i] - EPSILON[i]:
            return True
    return False

# Takes inn old coordinates and relative coordinates and outputs new coordinate
def calculateNewPosition(oldCoordinates, relCoordinates):
    # if isCoordinateOutside(relCoordinates): # This is wrong. If movement< build_area_min raises ValueError
    #     raise ValueError("Movement larger than build area or negativ")    
    if isCoordinateOutside(oldCoordinates):
        raise ValueError("Position outside of build area")

    newCoordinates = list(oldCoordinates)

    for i in range(3):        
        newCoordinates[i] = oldCoordinates[i] + relCoordinates[i]*direction[i]

        if (newCoordinates[i] < EPSILON[i] or newCoordinates[i] > BUILDING_AREA[i] - EPSILON[i]):
            direction[i] *= -1
            newCoordinates[i] = oldCoordinates[i] + relCoordinates[i]*direction[i]

    if (isCoordinateOutside(newCoordinates))
        raise ValueError("New position is outside of build area")            
    return newCoordinates

#Takes in coordinatearray and feedrate and returns gcode string
def coordinateToGCode_G0(newCoordinates, feedrate):
    return "G0 X"+str(newCoordinates[0])+" Y"+str(newCoordinates[1])+" Z"+str(newCoordinates[2])+" F"+str(feedrate)    

# Returns a gcode string to pause for given amount of milliseconds
def timeDelayToGCode_G4(milliSeconds):
    return "G4 P" + str(milliSeconds)

# Generates gCode from feedrate and distance and saves it in filename
def generateGCode(feedrateDistanceMatrix, filename):
    with open(filename, 'w') as file:
        file.write(";FLAVOR:UltiGCode\n;TIME:346\n;MATERIAL:43616\n;MATERIAL2:0\n;NOZZLE_DIAMETER:0.4\nM82\n")        
        file.write(coordinatesToGCode_G0(STARTPOSITION, 3600) + "\n")
        file.write(timeDelayToGCode_G4(1000) + "\n")
        coordinate = STARTPOSITION
        for pair in translateFeedrateDistanceMatrixToCoordinates(feedrateDistanceMatrix):
            if (isSilent(pair[0])):
                file.write(timeDelayToGCode_G4(pair[1]))
            else:
                coordinate = calculateNewPosition(coordinate, pair[0])
                file.write(coordinateToGCode_G0(coordinate, pair[1]) + "\n")
