import datetime as dt
import mido



miditextfile = open("test.csv", "w")
mid = mido.MidiFile("Midifiles/sekritstuffright.mid")
miditextfile.write(str(dt.datetime.now())+"\n")

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        if msg.type != "marker" and msg.type != "text":
            miditextfile.write(str(msg) + "\t\t;")
            miditextfile.write(str(msg.type)+"\n")
            print(msg, msg.type)

Hei = enumerate(mid.tracks)
print(Hei)
miditextfile.close() 