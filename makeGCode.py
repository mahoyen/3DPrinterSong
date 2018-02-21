import datetime as dt
import mido



miditextfile = open("test.csv", "w")
mid = mido.MidiFile("MarbleMachineRightHand.mid")
miditextfile.write(str(dt.datetime.now())+"\n")

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        miditextfile.write(str(msg) + ";")
        print(msg)

Hei = enumerate(mid.tracks)
print(Hei)
miditextfile.close() 