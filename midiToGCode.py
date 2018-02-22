# Imports
from mido import MidiFile
import sys

# Constants
MIDIFILENAME = "sekritstuffboth.mid"
FREQUENCYTOFEEDRATECONSTANT = 1
TIMETODISTANCECONSTANT = 1
BUILDING_AREA = [223, 223, 305] # [X, Y, Z]

# Global variables
direction = [1,1,1] # [X, Y, Z]

# Converts from miditoneNumber to frequency
def frequencyFromMidiNote(note):
    return 440*2**((note - 69)/12)

# Returns all the frequencies and durations from all the tone in filename
def getFrequencyTimeMatrix(filename):
    return [[frequencyFromMidiNote(msg.note), msg.time] for msg in MidiFile(MIDIFILENAME).tracks[1] if (msg.type == "note_on")]

# Converts frequency and time into feedrate and distance
def getFeedrateDistanceMatrix(frequencyTimeMatrix):
    return [[FREQUENCYTOFEEDRATECONSTANT*f, FREQUENCYTOFEEDRATECONSTANT*TIMETODISTANCECONSTANT*f/T] for f, T in frequencyTimeMatrix]

# Converts distances to coordinates
def translateFeedrateDistanceMatrixToCoordinates(feedrateDistanceMatrix):
    return [[relX, 0, 0] for feedrate, relX in feedrateDistanceMatrix]

# Returns relative coordinate-vector from distance
def translateDistanceToCoordinate(distance):
    return [distance, 0, 0]

# Takes inn old coordinates and relative coordinates and outputs new coordinate
def calculateNewPosition(oldCoordinates[3], relCoordinates[3]):

    newCoordinates = [oldCoordinates[0],oldCoordinates[1],oldCoordinates[2]]

    for i in range(3):
        if not(oldCoordinates[i] >= 0 and oldCoordinates < BUILDING_AREA[i]):
            raise Exception("Position outside of build area")
        if not(relCoordinates[i] >= 0 and relCoordinates < BUILDING_AREA[i]):
            raise Exception("Movement larger than build area or negativ")
        
        newCoordinates[i] = oldCoordinates[i] + relCoordinates[i]*direction[i]

        if (newCoordinates[i] >= 0 or newCoordinates[i] < BUILDING_AREA[i]):
            direction[i] *= -1
            newCoordinates[i] = oldCoordinates[i] + relCoordinates[i]*direction[i]
            if not(newCoordinates[i] < 0 and newCoordinates[i] > BUILDING_AREA[i]):
                raise Exception("New position is outside of build area")
    return newCoordinates[]

#Takes in coordinatearray and feedrate and outputs gcode string
def coordinatesToGCode_G0(newCoordinates[3], feedrate) 
    return gCodeLine = "G0 X"+str(newCoordinates[0])+" Y"+str(newCoordinate[1])+" Z"+str(newCoordinate[3])+" F"+str(feedrate)    
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

# Generates gCode from feedrate and distance and saves it in filename
def generateGCode(feedrateDistanceMatrix, filename):
    with open(filename, 'w') as file:
        file.write(";FLAVOR:UltiGCode\n;TIME:346\n;MATERIAL:43616\n;MATERIAL2:0\n;NOZZLE_DIAMETER:0.4\nM82\n")
        coordinates = [0, 0, 0]
        for pair in feedrateDistanceMatrix:
            coordinates = calculateNewPosition(coordinates, translateDistanceToCoordinate(pair[1]))
            file.write(coordinatesToGCode_G0(coordinates, pair[0]))      

        
# Genretates gCode from midifile
def generateGCodeFromMidi(midiFilename, gCodeFilename):
    movements = getFrequencyTimeMatrix(midiFilename)
    movements = getFeedrateDistanceMatrix(movements)
    generateGCode(movements, gCodeFilename)

def getFileExtension(filename):
        return filename.split('.')[-1]

def main():
    if len(sys.argv) != 3:
        print("midiToGCode requires two arguments: [midiFilename, gCodeFilename]")
        exit(1)    

    midFileExtension = getFileExtension(sys.argv[1])
    if midFileExtension.lower() != "mid":
        print("Midifile had extension ." + midFileExtension + ", expected .mid")
        exit(1)

    gCodeFileExtension = getFileExtension(sys.argv[2])
    if midFileExtension.lower() != "gcode":
        print("Midifile had extension ." + midFileExtension + ", expected .gcode")
        exit(1)
    try:
        generateGCode(sys.argv[1], sys.argv[2])
        print("gCode generated")
    except:
        print("Generation of gcode failed")
        exit(1)    

main()
