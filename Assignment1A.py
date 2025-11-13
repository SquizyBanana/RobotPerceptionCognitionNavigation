
measurements = []

for measurement in range(18):
    if measurement < 9:
        number = "0" + str(measurement+1)
    else:
        number = str(measurement+1)
    file = open(f"Assignment 1A data\MT_037004D1_0{number}-000.txt","r")

    raw_strings = file.readlines()

    for i in range(13):
        raw_strings.pop(0)
    strings = []
    for i in range(len(raw_strings)):
        strings.append(raw_strings[i].split("\t"))

    total_x = 0
    total_y = 0
    total_z = 0
    total_gx = 0
    total_gy = 0
    total_gz = 0


    for i in range(len(strings)):
        total_x = total_x+float(strings[i][2])
        total_y = total_y+float(strings[i][3])
        total_z = total_z+float(strings[i][4])
        total_gx = total_gx+float(strings[i][5])
        total_gy = total_gy+float(strings[i][6])
        total_gz = total_gz+float(strings[i][7])

    average_x = total_x/len(strings)
    average_y = total_y/len(strings)
    average_z = total_z/len(strings)
    average_gx = total_gx/len(strings)
    average_gy = total_gy/len(strings)
    average_gz = total_gz/len(strings)

    average_list = [average_x, average_y, average_z, average_gx, average_gy, average_gz]

    measurements.append(average_list)

print(measurements)

# 1, 7, 13 +x