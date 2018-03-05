# Imports
from mido import MidiFile
import datetime as dt

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

def getDuration(track):
    duration = 0
    for msg in track:
        if msg.type != "marker" and msg.type != "text":
            duration += msg.time
    return duration/480

def printTrack(track, filename):
    miditextfile = open(filename, "w")
    miditextfile.write(str(dt.datetime.now())+"\n")

    for msg in track:
        try:
            miditextfile.write("type=" + str(msg.type) + "\t note=" + str(msg.note) + "\t time=" + str(msg.time) + "\n")
        except:
            miditextfile.write(str(msg) + "\n")

    miditextfile.close() 

def cleanupTrack(track):
    i = 0
    length = len(track) - 1
    while i < length:
        if (track[i].type != "note_on" and track[i].type != "note_off"):
            track[i + 1].time += track.pop(i).time
            length -= 1
        else:
            i += 1
    
    track.pop(-1)

