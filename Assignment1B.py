import numpy as np
import matplotlib.pyplot as plt


measurements = []
plt.style.use('_mpl-gallery')

file1 = open("RobotPerceptionCognitionNavigation\Assingment 1B data\imu_417.csv","r")
file2 = open("RobotPerceptionCognitionNavigation\Assingment 1B data\imu_423.csv","r")
file3 = open("RobotPerceptionCognitionNavigation\Assingment 1B data\imu_425.csv","r")

files = [file1,file2,file3]

file_values = []
for file in files:
    raw_strings = file.readlines()
    raw_strings.pop(0)
    x_accel = []
    y_accel = []
    z_accel = []
    x_rot = []
    y_rot = []
    z_rot = []
    time = float(raw_strings[0].split(",")[0])
    print(time)
    for i in range(len(raw_strings)):
        numbers = raw_strings[i].split(",")
        delta_time = float(numbers[0]) - time
        time = float(numbers[0])
        x_accel.append(float(numbers[4])*delta_time)
        y_accel.append(float(numbers[5])*delta_time)
        z_accel.append(float(numbers[6])*delta_time)
        x_rot.append(float(numbers[1])*delta_time)
        y_rot.append(float(numbers[2])*delta_time)
        z_rot.append(float(numbers[3])*delta_time)
        #if (float(numbers[3]) >= 10): (print(float(numbers[3])))
    file_values.append([x_accel,y_accel,z_accel,x_rot,y_rot,z_rot])

fig, ax = plt.subplots()


# ax.plot(file_values[0][4], "r")
# ax.plot(file_values[0][5], "g")
# ax.plot(file_values[0][6], "b")

integrated_z_angles = []
for i in range(len(file_values)):
    current_z_angle = 0
    integrated_z_angle = []
    for t in range(len(file_values[0][5])):
        current_z_angle += file_values[i][5][t]
        integrated_z_angle.append(current_z_angle)
    integrated_z_angles.append(integrated_z_angle)


ax.plot(integrated_z_angles[0], "r")
ax.plot(integrated_z_angles[1], "b")
ax.plot(integrated_z_angles[2], "g")


plt.show()