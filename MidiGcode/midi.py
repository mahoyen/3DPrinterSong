# Imports
from mido import MidiFile

# Converts from miditoneNumber to frequency
def frequencyFromMidiNote(note):
    if (note == 0):
        return 0
    return 440*2**((note - 69)/12)

def pushQueue(queue, element):
    queue.append(element)
    return queue[-2:]

# Returns list of 2-tuples of a list of notes and the duration. list[list(list[note 1, note 2], duration)]
def getNotesTimeMatrix(track):
    notesTimeMatrix = list()
    currentNotes = [0, 0]
    for i, msg in enumerate(track[:-1]):
        if msg.type == "note_on":
            currentNotes = pushQueue(currentNotes, msg.note)
        elif msg.type == "note_off":
            try:
                currentNotes[currentNotes.index(msg.note)] = 0
            except:
                pass
                # print(str(msg.note) + " not currently playing")
        else:
            raise ValueError("Message types should be note_on or note_off")

        if track[i + 1].time != 0:
            notesTimeMatrix.append([[currentNotes[0], currentNotes[1], 0], track[i + 1].time/480])
    return notesTimeMatrix

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
    return track

# Returns all the frequencies and durations from all the tones in filename. list[list(list[freq 1, freq 2, freq 3], duration)]
def getFrequencyTimeMatrix(filename):
    mid = MidiFile(filename).tracks[0]
    notesTimeMatrix = getNotesTimeMatrix(cleanupTrack(mid))    

    frequencyTimeMatrix = []
    for noteLine in notesTimeMatrix:
        freqLine = list(noteLine)
        for i in range(len(noteLine[0])):
            freqLine[0][i] = frequencyFromMidiNote(noteLine[0][i])
        frequencyTimeMatrix.append(freqLine)    
    
    return frequencyTimeMatrix

def getDuration(track):
    duration = 0
    for msg in track:
        if msg.type != "marker" and msg.type != "text":
            duration += msg.time
    return duration/480

def printTrack(track, filename):
    miditextfile = open(filename, "w")   

    for msg in track:
        try:
            miditextfile.write("type=" + str(msg.type) + "\t note=" + str(msg.note) + "\t time=" + str(msg.time) + "\n")
        except:
            miditextfile.write(str(msg) + "\n")

    miditextfile.close()
