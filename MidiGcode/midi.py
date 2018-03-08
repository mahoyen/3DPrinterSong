# Imports
from mido import MidiFile
import datetime as dt

# Converts from miditoneNumber to frequency
def frequencyFromMidiNote(note):
    return 440*2**((note - 69)/12)

def pushQueue(queue, element):
    queue.append(element)
    return queue[-2:]

# Returns list of 2-tuples of a list of notes and the duration. list[list(list[note 1, note 2], duration)]
def getNotes(track):
    returnList = {}
    currentNotes = [0, 0]
    for i, msg in enumerate(track):
        if msg.type == "note_on":
            currentNotes = pushQueue(currentNotes, msg.note)
        elif msg.type == "note_off":
            currentNotes[currentNotes.index(msg.note)] = 0
        else:
            raise ValueError("Message types should be note_on or note_off")

        if track[i + 1].time != 0:
            returnList.append([currentNotes, track[i + 1].time])
    return returnList

# Returns track with just note_on and note_off messages
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

# Returns all the frequencies and durations from all the tones in filename. list[list(list[freq 1, freq 2], duration)]
def getFrequencyTimeMatrix(filename):
    mid = MidiFile(filename).tracks[0]
    notes = getNotes(cleanupTrack(mid))
    for msg in notes:
        for freq in msg[0]:
            freq = frequencyFromMidiNote(freq)

    return notes

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
