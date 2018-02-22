# Imports
from mido import MidiFile

# Constants
MIDIFILENAME = "sekritstuffboth.mid"
FREQUENCYTOFEEDRATECONSTANT = 1
TIMETODISTANCECONSTANT = 1
BUILDING_AREA = [223, 223, 305]

# Global variables
direction = [1,1,1]

# Converts from miditoneNumber to frequency
def frequencyFromMidiNote(note):
    return 440*2**((note - 69)/12)

# Returns all the frequencies and durations from all the tone in filename
def getFrequencyTimeVector(filename):
    return [[frequencyFromMidiNote(msg.note), msg.time] for msg in MidiFile(MIDIFILENAME).tracks[1] if (msg.type == "note_on")]

# Converts frequency and time into feedrate and distance
def getFeedrateDistanceVector(frequencyTimeVector):
    return [[FREQUENCYTOFEEDRATECONSTANT*f, FREQUENCYTOFEEDRATECONSTANT*TIMETODISTANCECONSTANT*f/T] for f, T in frequencyTimeVector]


# Takes inn old coordinates and relative coordinates and outputs new coordinate
def calculateNewPosition(oldCoordinates[3], relCoordinates[3]) {
    
    
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
}

#Takes in coordinatearray and feedrate and outputs gcode string
def coordinatesToGCode_G0(newCoordinates[3], feedrate) {
    return gCodeLine = "G0 X"+str(newCoordinates[0])+" Y"+str(newCoordinate[1])+" Z"+str(newCoordinate[3])+" F"+str(feedrate)    
}

# Generates gCode from feedrate and distance and saves it in filename
def generateGCode(feedrateDistancevector, filename):
    with open(filename, 'w') as file:
        file.write(";FLAVOR:UltiGCode\n;TIME:346\n;MATERIAL:43616\n;MATERIAL2:0\n;NOZZLE_DIAMETER:0.4\nM82\n")

        

# Genretates gCode from midifile
def generateGCodeFromMidi(midiFilename, gCodeFilename):
    movements = getFrequencyTimeVector(midiFilename)
    movements = getFeedrateDistanceVector(movements)
    return generateGCode(movements, gCodeFilename)

generateGCode(MIDIFILENAME, "a.gcode")
print("gCode generated")
