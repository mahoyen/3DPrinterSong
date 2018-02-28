import datetime as dt
import mido



miditextfile = open("midifromMido.txt", "w")
mid = mido.MidiFile("sekritstuffleft.mid")
miditextfile.write(str(dt.datetime.now())+"\n")

for i, track in enumerate(mid.tracks):
    print('Track {}: {}'.format(i, track.name))
    for msg in track:
        if not(msg.type == "control_change"):
            miditextfile.write(str(msg) + "\n")
            print(msg)

#Hei = enumerate(mid.tracks)
#print(Hei)
miditextfile.close() 