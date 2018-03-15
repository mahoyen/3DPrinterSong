import json

# Printer settings
BUILDING_AREA = [223, 223, 305]
EPSILON = [10, 10, 10]
STARTPOSITION = [210, 210, 100]

# Song settings
FREQUENCYTOFEEDRATECONSTANT = 1
TIMETODISTANCECONSTANT = 1
TRACK = 0

def update(filename):
    if filename[-4:] != "json":
        raise ValueError("Config file must be a json file")
    try:
        with open(filename) as file:
            input = json.load(file)
    except:
        raise ValueError("Config file must be in json format")
    
    buildArea = input["printer"]["buildArea"]
    global BUILDING_AREA
    BUILDING_AREA = [buildArea["x"], buildArea["y"], buildArea["z"]]

    epsilon = input["printer"]["epsilon"]
    global EPSILON
    EPSILON = [epsilon["x"], epsilon["y"], epsilon["z"]]

    global FREQUENCYTOFEEDRATECONSTANT
    FREQUENCYTOFEEDRATECONSTANT = input["song"]["frequencyScaleConstant"]
    global TIMETODISTANCECONSTANT
    TIMETODISTANCECONSTANT = input["song"]["timeScaleConstant"]
    global TRACK
    TRACK = input["song"]["track"]

    startposition = input["song"]["startposition"]
    global STARTPOSITION
    STARTPOSITION = [startposition["x"], startposition["y"], startposition["z"]]

update("MidiGCodeConfig.json")

'''
print(BUILDING_AREA)
print(EPSILON)
print(STARTPOSITION)

print(FREQUENCYTOFEEDRATECONSTANT)
print(TIMETODISTANCECONSTANT)
print(TRACK)
'''
