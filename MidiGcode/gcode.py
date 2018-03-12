# Constants 

FREQUENCYTOFEEDRATECONSTANT = 7
TIMETODISTANCECONSTANT = 0.07
BUILDING_AREA = [223, 223, 305] # [X, Y, Z]
EPSILON = [10, 10, 10] # [X, Y, Z]
STARTPOSITION = [210, 210, 100] # [X, Y, Z]

# Global variables
direction = [1,1,1] # [X, Y, Z]

# Returns true if all notes in noteList are zero
def isAllZeros(liste):
    for i in liste:
        if i != 0:
            return False
    return True

# Converts frequencies returns list[list[list[feedrateX, feedrateY, feedrateZ], feedrate]]
def translateFrequencyTimeMatrixToFeedratesTimeMatrix(frequencyTimeMatrix):
    feedrateTimeMatrix = list()
    for frequencies, time in frequencyTimeMatrix:
        feedrates = list(frequencies)
        for i in range(len(frequencies)):
            feedrates[i] = FREQUENCYTOFEEDRATECONSTANT * frequencies[i]
        feedrateTimeMatrix.append([feedrates, time])
    
    return feedrateTimeMatrix
    
#Takes feedratelist and returns absolutelength the list  
def calculateAbsoluteFeedrate(feedrates):
    sumFeedrateSquared = 0
    for i in range(len(feedrates)):
        sumFeedrateSquared += feedrates[i]**2
    return sumFeedrateSquared**0.5

# Returns True if coordinate is outside build area
def isCoordinateOutside(coordinate):
    for i in range(len(coordinate)):
        if coordinate[i] < EPSILON[i] or coordinate[i] > BUILDING_AREA[i] - EPSILON[i]:
            return True
    return False

def findLongestDistanceAndSaturate(oldCoordinate, relCoordinate, i):
    if ((BUILDING_AREA[i])/2 < oldCoordinate[i]):
        return EPSILON[i]
    else:
        return BUILDING_AREA[i] - EPSILON[i]

# Takes inn old coordinates and relative coordinates and outputs new coordinate
def calculateNewPosition(oldCoordinate, relCoordinate):
    # if isCoordinateOutside(relCoordinate): # This is wrong. If movement< build_area_min raises ValueError
    #     raise ValueError("Movement larger than build area or negativ")
    if isCoordinateOutside(oldCoordinate):
        raise ValueError("Position outside of build area")

    newCoordinate = list(oldCoordinate)

    for i in range(3):        
        newCoordinate[i] = oldCoordinate[i] + relCoordinate[i] #*direction[i]

        if (newCoordinate[i] < EPSILON[i] or newCoordinate[i] > BUILDING_AREA[i] - EPSILON[i]):
            #direction[i] *= -1
            newCoordinate[i] = oldCoordinate[i] - relCoordinats[i] #*direction[i]

            if (newCoordinate[i] < EPSILON[i] or newCoordinate[i] > BUILDING_AREA[i] - EPSILON[i]):
                newCoordinate[i] = findLongestDistanceAndSaturate(oldCoordinate[i], relCoordinate[i], i)

    if isCoordinateOutside(newCoordinate):
        raise ValueError("New position outside of build area")
        
    return newCoordinate

#Takes in coordinatearray and feedrate and returns gcode string
def coordinateToGCode_G0(newCoordinate, feedrate):
    return "G0 X"+str(newCoordinate[0])+" Y"+str(newCoordinate[1])+" Z"+str(newCoordinate[2])+" F"+str(feedrate)    

# Returns a gcode string to pause for given amount of milliseconds
def timeDelayToGCode_G4(milliSeconds):
    if milliSeconds:
        return "G4 P" + str(milliSeconds) + "\n"
    return ""

def calculateRelCoordinates(feedrates, time):
    relCoordinate = list(feedrates)
    for i in range(len(feedrates)):
        relCoordinate[i] = feedrates[i]*time*TIMETODISTANCECONSTANT
    return relCoordinate

# Generates gCode from feedrate and time and saves it in filename
def generateGCode(feedratesTimeMatrix, filename):
    with open(filename, 'w') as file:
        file.write(";FLAVOR:UltiGCode\n;TIME:346\n;MATERIAL:43616\n;MATERIAL2:0\n;NOZZLE_DIAMETER:0.4\nM82\n")        
        file.write(coordinateToGCode_G0(STARTPOSITION, 3600) + "\n")
        file.write(timeDelayToGCode_G4(1000))
        oldCoordinate = STARTPOSITION
        for feedrates, time in feedratesTimeMatrix:
            if (isAllZeros(feedrates)):
                file.write(timeDelayToGCode_G4(time))
            else:
                relCoordinate = calculateRelCoordinates(feedrates, time)
                absoluteFeedrate = calculateAbsoluteFeedrate(feedrates)
                newCoordinate = calculateNewPosition(oldCoordinate, relCoordinate)
                file.write(coordinateToGCode_G0(newCoordinate, absoluteFeedrate) + "\n")
                oldCoordinate = newCoordinate
