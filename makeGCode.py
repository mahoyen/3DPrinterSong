import datetime

gcode_file = open("test.gcode", "w")

gcode_file.write("Hello World") 
gcode_file.write("This is our new text file") 
gcode_file.write("and this is another line.") 
gcode_file.write("Why? Because we can.") 
 
gcode_file.close() 