import numpy as np
measurements = []

for measurement in range(18):
    if measurement < 9:
        number = "0" + str(measurement+1)
    else:
        number = str(measurement+1)
    file = open(f"Assignment 1B data\TBD","r")

    raw_strings = file.readlines()

    for i in range(13):
        raw_strings.pop(0)
    strings = []
    for i in range(len(raw_strings)):
        strings.append(raw_strings[i].split("\t"))