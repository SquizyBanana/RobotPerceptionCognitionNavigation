import numpy as np
measurements = []


file1 = open("RobotPerceptionCognitionNavigation\Assingment 1B data\imu_417.csv","r")
file2 = open("RobotPerceptionCognitionNavigation\Assingment 1B data\imu_423.csv","r")
file3 = open("RobotPerceptionCognitionNavigation\Assingment 1B data\imu_425.csv","r")

files = [file1,file2,file3]

file_strings = []
for file in files:
    raw_strings = file.readlines()
    raw_strings.pop(0)
    strings = []
    for i in range(len(raw_strings)):
        strings.append(raw_strings[i].split(","))
    file_strings.append(strings)

print(file_strings)