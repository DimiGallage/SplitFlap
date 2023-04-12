import bpy
import csv
from math import *

# Parameters:
# Number of flaps
Flaps = 16
# names of input shafts, from least significant to most significant
Shafts = ["Circle", "Circle.001", "Circle.002", "Circle.003", "Circle.004", "Circle.005", "Circle.006", "Circle.007",
          "Circle.008", "Circle.009", "Circle.010", "Circle.011", "Circle.012", "Circle.013", "Circle.014", "Circle.015",
          "Circle.016", "Circle.017", "Circle.018", "Circle.019", "Circle.020", "Circle.021", "Circle.022", "Circle.023",
          "Circle.024", "Circle.025", "Circle.026", "Circle.027", "Circle.028", "Circle.029", "Circle.030", "Circle.031",
          "Circle.032", "Circle.033", "Circle.034", "Circle.035", "Circle.036", "Circle.037", "Circle.038", "Circle.039",
          "Circle.040", "Circle.041", "Circle.042", "Circle.043", "Circle.044", "Circle.045", "Circle.046", "Circle.047",
          "Circle.048", "Circle.049", "Circle.050", "Circle.051", "Circle.052", "Circle.053", "Circle.054", "Circle.055",
          "Circle.056", "Circle.057", "Circle.058", "Circle.059", "Circle.060", "Circle.061", "Circle.062", "Circle.063",
          "Circle.064", "Circle.065", "Circle.066", "Circle.067", "Circle.068", "Circle.069", "Circle.070", "Circle.071",
          "Circle.072"]
# Number of frames per 1 digit
FramesPerDigit = 10
# Number of frames per pause
FramesPerPause = 20
# Sequence of numbers to display
NumbersToDisplay = []

with open('dimdim.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count < 5:
            NumbersToDisplay.append(row[0]+row[1].zfill(9))
        else:
            break
        line_count += 1
# End of parameters


# Auxiliary functions
def ClearAnimationData():
    for objname in Shafts:
        obj = bpy.data.objects[objname]
        obj.animation_data_clear()
        
# pin to current frame
def PinToCurrentFrame(FrameCount):
    for objname in Shafts:
        obj = bpy.data.objects[objname]
        obj.keyframe_insert(data_path="rotation_euler", frame=FrameCount, index=1) # y only

# from degrees to radians
def rads( angle ):
    return angle * pi / 180

def DisplayNumber( number ):
    # split number into digits. Number of digits = number of shafts
    for i in range(0, len(Shafts) ):
        if(number[i].isalpha()):
            currentdigits[i] = ord(number[i]) - 87
        else:
            currentdigits[i] = int(number[i])
        obj = bpy.data.objects[Shafts[i]]
        obj.rotation_euler.y = rads( - 360/Flaps * currentdigits[i])

    
ClearAnimationData()

FrCount = 1

currentdigits = [0 for i in Shafts] 

# display initial number
DisplayNumber( NumbersToDisplay[0] )
PinToCurrentFrame(FrCount)

for i in range(1, len(NumbersToDisplay)):
    
    # change current number to the next number digit by digit until they are the same
    while True:
        NewNumber = NumbersToDisplay[i]
        # compare current with new digits
        done = True
        for j in range(0, len(Shafts)):

            if (NewNumber[j].isalpha()):
                newdigit = ord(NewNumber[j]) - 87
            else:
                newdigit = int(NewNumber[j])

            if newdigit != currentdigits[j]:
                done = False
                currentdigits[j] = (currentdigits[j] + 1) % Flaps;
                obj = bpy.data.objects[Shafts[j]]
                obj.rotation_euler.y -= rads( 360/Flaps )
        
        FrCount += FramesPerDigit
        PinToCurrentFrame(FrCount)

        if done:
            break
    
    FrCount += FramesPerPause
    PinToCurrentFrame(FrCount)    
        


# and finally, make everything linear instead of bezier
for objname in Shafts:
    obj = bpy.data.objects[objname]
    fcurves = obj.animation_data.action.fcurves
    for fcurve in fcurves:
        for kf in fcurve.keyframe_points:
            kf.interpolation = 'LINEAR'  

# Adjust total frame count in this animation
bpy.data.scenes[0].frame_end = FrCount

