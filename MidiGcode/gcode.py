# Constants
FREQUENCYTOFEEDRATECONSTANT = 1
TIMETODISTANCECONSTANT = 1
BUILDING_AREA_MAX = [223, 223, 305] # [X, Y, Z]
BUILDING_AREA_MIN = [10, 10, 10]
STARTPOSITION = [100, 100, 100] # [X, Y, Z]

# Global variables
direction = [1,1,1] # [X, Y, Z]

# Converts frequency and time into feedrate and distance
def getFeedrateDistanceMatrix(frequencyTimeMatrix):
    return [[float(FREQUENCYTOFEEDRATECONSTANT*f), float(FREQUENCYTOFEEDRATECONSTANT*TIMETODISTANCECONSTANT*f/T)] for f, T in frequencyTimeMatrix]

# Converts distances to coordinates
def translateFeedrateDistanceMatrixToCoordinates(feedrateDistanceMatrix):
    return [[relX, 0, 0] for feedrate, relX in feedrateDistanceMatrix]

# Returns relative coordinate-vector from distance
def translateDistanceToCoordinate(distance):
    return [distance, 0, 0]

# Returns True if coordinate is inside build area
def isCoordinateInside(coordinate):
    for i in coordinate:
        if i < BUILDING_AREA_MIN or i > BUILDING_AREA_MAX:
            return False
    return True

# Takes inn old coordinates and relative coordinates and outputs new coordinate
def calculateNewPosition(oldCoordinates, relCoordinates):

    newCoordinates = list(oldCoordinates)

    for i in range(3):
        if not(oldCoordinates[i] >= 0 and oldCoordinates[i] < BUILDING_AREA[i]):
            raise Exception("Position outside of build area")
        if not(relCoordinates[i] >= 0 and relCoordinates[i] < BUILDING_AREA[i]):
            raise Exception("Movement larger than build area or negativ")
        
        newCoordinates[i] = oldCoordinates[i] + relCoordinates[i]*direction[i]

        if (newCoordinates[i] < 0 or newCoordinates[i] > BUILDING_AREA[i]):
            direction[i] *= -1
            newCoordinates[i] = oldCoordinates[i] + relCoordinates[i]*direction[i]
            if not(newCoordinates[i] >= 0 and newCoordinates[i] <= BUILDING_AREA[i]):
                raise Exception("New position is outside of build area")
    return newCoordinates

#Takes in coordinatearray and feedrate and outputs gcode string
def coordinatesToGCode_G0(newCoordinates, feedrate):
    return "G0 X"+str(newCoordinates[0])+" Y"+str(newCoordinates[1])+" Z"+str(newCoordinates[2])+" F"+str(feedrate)    
'''
def master(midifilename, gcodeFilename, startingCoordinates):
    feedrateDistanceMatrix = getFeedrateDistanceMatrix(getFrequencyTimeMatrix(midifilename))
    feedrateMatrix = [[feedrate] for feedrate, distanse in feedrateDistanceMatrix]
    coordinates = translateFeedrateDistanceMatrixToCoordinates(feedrateDistanceMatrix)

    for i in range(len(coordinates)):
        if (not i):
            oldCoordinates[i] = startingCoordinates
        else:
            
            newPosition = calculateNewPosition(oldCoordinates[i], coordinates[i])
'''

# Returns a gcode string to pause for given amount of milliseconds
def timeDelayToGCode_G4(milliSeconds):
    return "G4 P" + str(milliSeconds)

# Generates gCode from feedrate and distance and saves it in filename
def generateGCode(feedrateDistanceMatrix, filename):
    with open(filename, 'w') as file:
        file.write(";FLAVOR:UltiGCode\n;TIME:346\n;MATERIAL:43616\n;MATERIAL2:0\n;NOZZLE_DIAMETER:0.4\nM82\n")        
        file.write(coordinatesToGCode_G0(STARTPOSITION, 3600) + "\n")
        coordinates = STARTPOSITION
        for pair in feedrateDistanceMatrix:
            coordinates = calculateNewPosition(coordinates, translateDistanceToCoordinate(pair[1]))
            file.write(coordinatesToGCode_G0(coordinates, pair[0]) + "\n")      
