# Imports
from mido import MidiFile

# Constants
MIDIFILENAME = "sekritstuffboth.mid"
FREQUENCYTOFEEDRATECONSTANT = 1
TIMETODISTANCECONSTANT = 1

# Converts from miditoneNumber to frequency
def frequencyFromMidiNote(note):
    return 440*2**((note - 69)/12)

# Returns all the frequencies and durations from all the tone in filename
def getFrequencyTimeVector(filename):
    return [[frequencyFromMidiNote(msg.note), msg.time] for msg in MidiFile(MIDIFILENAME).tracks[1] if (msg.type == "note_on")]

# Converts frequency and time into feedrate and distance
def getFeedrateDistanceVector(frequencyTimeVector):
    return [[FREQUENCYTOFEEDRATECONSTANT*f, FREQUENCYTOFEEDRATECONSTANT*TIMETODISTANCECONSTANT*f/T] for f, T in frequencyTimeVector]

# Generates gCode from feedrate and distance and saves it in filename
def generateGCode(feedrateDistancevector, filename):
    with open(filename, 'w') as file:
        file.write(";FLAVOR:UltiGCode\n;TIME:13551\n;MATERIAL:43616\n;MATERIAL2:0\n;NOZZLE_DIAMETER:0.4")

# Genretates gCode from midifile
def generateGCodeFromMidi(midiFilename, gCodeFilename):
    movements = getFrequencyTimeVector(midiFilename)
    movements = getFeedrateDistanceVector(movements)
    return generateGCode(movements, gCodeFilename)

generateGCode(MIDIFILENAME, "a.gcode")
print("gCode generated")
