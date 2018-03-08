# Imports
import sys
from MidiGcode import midi, gcode
from mido import MidiFile
        
# Genretates gCode from midifile
def generateGCodeFromMidi(midiFilename, gCodeFilename):
    frequencyTimeMatrix = midi.getFrequencyTimeMatrix(midiFilename)
    #print("Frequency, Time")
    #for line in frequencyTimeMatrix:
    #    print(line[0], line[1])
    coordinates = gcode.translateFrequencyTimeMatrixToCoordinates(frequencyTimeMatrix)
    #print("Relative Coordinates")
    #for c in coordinates:
    #    print(c[0], c[1], sep='\t')

    gcode.generateGCode(coordinates, gCodeFilename)

def getFileExtension(filename):
        return filename.split('.')[-1]

def main():
    if len(sys.argv) != 3:
        print("midiToGCode requires two arguments: [midiFilename, gCodeFilename]")
        exit(1)    

    midFileExtension = getFileExtension(sys.argv[1])
    if midFileExtension.lower() != "mid":
        print("MidiFilename argument had extension ." + midFileExtension + ", expected .mid")
        exit(1)

    gCodeFileExtension = getFileExtension(sys.argv[2])
    if gCodeFileExtension.lower() != "gcode":
        print("GcodeFilename argument had extension ." + gCodeFileExtension + ", expected .gcode")
        exit(1)

    #try:
    generateGCodeFromMidi(sys.argv[1], sys.argv[2])
    print("gCode generated")
    #except Exception as e:
    #print("Generation of gcode failed "+str(e))
    exit(1)

main()