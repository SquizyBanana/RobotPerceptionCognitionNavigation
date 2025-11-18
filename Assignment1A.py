import numpy as np
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
meas = np.array(measurements)

g = 9.81
omega_e = 7.292115e-5
phi_deg = 52.21833
omega_ref = omega_e * np.sin(np.deg2rad(phi_deg))

def bias_scale(f_up, f_down, ref):
    b = 0.5*(f_up + f_down)
    S = (f_up - f_down - 2 * ref)/(2 * ref)
    return b, S

orient = {"z_up":   0,"z_down": 1,"y_down": 2,"y_up":   3,"x_down": 4,"x_up":   5,}

acc_col = {"x": 0, "y": 1, "z": 2}
gyr_col = {"x": 3, "y": 4, "z": 5}

axis_updown = {"x": ("x_up", "x_down"),"y": ("y_up", "y_down"),"z": ("z_up", "z_down"),}

acc_bias = {"x": [], "y": [], "z": []}
acc_sf   = {"x": [], "y": [], "z": []}
gyr_bias = {"x": [], "y": [], "z": []}
gyr_sf   = {"x": [], "y": [], "z": []}

for run in range(3):
    base = run * 6
    for ax in ["x", "y", "z"]:
        a_idx = acc_col[ax]
        g_idx = gyr_col[ax]

        up_name, down_name = axis_updown[ax]
        up_idx   = base + orient[up_name]
        down_idx = base + orient[down_name]

        f_up = meas[up_idx, a_idx]
        f_down = meas[down_idx, a_idx]
        b_a, S_a = bias_scale(f_up, f_down, g)
        acc_bias[ax].append(b_a)
        acc_sf[ax].append(S_a)

        w_up = meas[up_idx, g_idx]
        w_down = meas[down_idx, g_idx]
        b_g, S_g = bias_scale(w_up, w_down, omega_ref)
        gyr_bias[ax].append(b_g)
        gyr_sf[ax].append(S_g)

for ax in ["x", "y", "z"]:
    acc_bias[ax] = np.array(acc_bias[ax])
    acc_sf[ax]   = np.array(acc_sf[ax])
    gyr_bias[ax] = np.array(gyr_bias[ax])
    gyr_sf[ax]   = np.array(gyr_sf[ax])

print("Axis | b_a [m/s^2] | S_a [no unit?] | b_g [rad/s] | S_g [no unit?]")
for ax in ["x", "y", "z"]:
    b_a_mean = acc_bias[ax].mean()
    S_a_mean = acc_sf[ax].mean()
    b_g_mean = gyr_bias[ax].mean()
    S_g_mean = gyr_sf[ax].mean()
    print(f"{ax.upper():>4} | {b_a_mean:10.6f} | {S_a_mean:8.6f} | {b_g_mean:11.8f} | {S_g_mean:8.6f}")

print("Axis | std(b_a) | std(S_a) | std(b_g) | std(S_g)")
for ax in ["x", "y", "z"]:
    b_a_std = acc_bias[ax].std(ddof=1)
    S_a_std = acc_sf[ax].std(ddof=1)
    b_g_std = gyr_bias[ax].std(ddof=1)
    S_g_std = gyr_sf[ax].std(ddof=1)
    print(f"{ax.upper():>4} | {b_a_std:8.6f} | {S_a_std:8.6f} | {b_g_std:10.8f} | {S_g_std:8.6f}")

# 1, 7, 13 +x?
# I thought this:
# 1: z-axis up from the table (so pointing against gravity)
#2: z-axis down (same direction as gravity)
#3: y-axis down (so same direction as gravity)
#4: y-axis up (against gravity)
#5: x-axis down (so same direction as gravity)
#6: x-axis up (against gravity)
