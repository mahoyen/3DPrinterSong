import midi

# Constants 

FREQUENCYTOFEEDRATECONSTANT = 1
TIMETODISTANCECONSTANT = 0.09
BUILDING_AREA = [223, 223, 305] # [X, Y, Z]
EPSILON = [10, 10, 10] # [X, Y, Z]
STARTPOSITION = [10, 10, 100] # [X, Y, Z]

# Global variables
direction = [1,1,1] # [X, Y, Z]


# Converts distances to coordinates. returns list[list[list[x, y, z], feedrate]]
+def translateFrequencyTimeMatrixToCoordinates(frequencyTimeMatrix):
    coordinateFeedrateMatrix = list()
    for frequencies, time in frequencyTimeMatrix:
        sumFeedrate = 0
        feedrates = list(frequencies)
        for i in range(len(frequencies)):
            feedrates[i] = FREQUENCYTOFEEDRATECONSTANT * frequencies[i]
            sumFeedrate += feedrates[i]**2
        absoluteFeedrate = sumFeedrate**0.5
        duration = TIMETODISTANCECONSTANT*absoluteFeedrate/time
        coordinateFeedrateMatrix.append([[feedrate*duration for feedrate in feedrates], absoluteFeedrate])
    
    return coordinateFeedrateMatrix
    # return [[relX, 0, 0] for feedrate, relX in feedrateDistanceMatrix]


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
    print(relCoordinates)

    for i in range(3):        
        newCoordinates[i] = oldCoordinates[i] + relCoordinates[i] #*direction[i]

        if (newCoordinates[i] < EPSILON[i] or newCoordinates[i] > BUILDING_AREA[i] - EPSILON[i]):
            #direction[i] *= -1
            newCoordinates[i] = oldCoordinates[i] - relCoordinates[i] #*direction[i]

    if (isCoordinateOutside(newCoordinates)):        
        print(relCoordinates)
        print(oldCoordinates)
        print(newCoordinates)
        raise ValueError("New position is outside of build area")            
    return newCoordinates

#Takes in coordinatearray and feedrate and returns gcode string
def coordinateToGCode_G0(newCoordinates, feedrate):
    return "G0 X"+str(newCoordinates[0])+" Y"+str(newCoordinates[1])+" Z"+str(newCoordinates[2])+" F"+str(feedrate)    

# Returns a gcode string to pause for given amount of milliseconds
def timeDelayToGCode_G4(milliSeconds):
    if milliSeconds:
        return "G4 P" + str(milliSeconds) + "\n"
    return ""

# Generates gCode from feedrate and distance and saves it in filename
def generateGCode(coordinateFeedrateMatrix, filename):
    with open(filename, 'w') as file:
        file.write(";FLAVOR:UltiGCode\n;TIME:346\n;MATERIAL:43616\n;MATERIAL2:0\n;NOZZLE_DIAMETER:0.4\nM82\n")        
        file.write(coordinateToGCode_G0(STARTPOSITION, 3600) + "\n")
        file.write(timeDelayToGCode_G4(1000))
        coordinate = STARTPOSITION
        for coordinates, feedrate in coordinateFeedrateMatrix:
            if (mdid.isSilent(feedrate)):
                file.write(timeDelayToGCode_G4(feedrate))
            else:
                coordinate = calculateNewPosition(coordinate, coordinates)
                file.write(coordinateToGCode_G0(coordinate, feedrate) + "\n")
