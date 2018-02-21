import datetime as dt
import py-midi

gcode_file = open("test.gcode", "w")

gcode_file.write(";"+str(dt.datetime.now())+"\n") 

gcode_file.close() 