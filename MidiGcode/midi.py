# Imports
from mido import MidiFile

# Converts from miditoneNumber to frequency
def frequencyFromMidiNote(note):
    return 440*2**((note - 69)/12)

# Returns all the frequencies and durations from all the tone in filename
def getFrequencyTimeMatrix(filename):
    '''
    frequencyTimeMatrix = list()
    i = 0
    for msg in MidiFile(filename).tracks[0]:
        if (msg.type == "note_on"):
            frequency = frequencyFromMidiNote(msg.note)
            time = msg.time
            frequencyTimeVector = [frequency, time]
            print(frequencyTimeVector)
            frequencyTimeMatrix[i] = frequencyTimeVector
            i += 1
    '''
    return [[frequencyFromMidiNote(msg.note), msg.time] for msg in MidiFile(filename).tracks[0] if (msg.type == "note_on" and msg.time is not 0)  ]
