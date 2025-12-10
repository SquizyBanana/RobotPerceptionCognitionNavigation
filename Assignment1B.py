import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# the accelerometer bias (m/s^2)
accelerometer_bias = np.array([-0.035453, 0.060675, -0.006935])
# the accelerometer scale (no unit)
accelerometer_scale = np.array([0.000421, -0.000239, 0.000230])

# the gyroscope bias (rad/s)
gyroscope_bias = np.array([-0.00584872, -0.00015131, -0.00231847])
# the gyroscope scale, we set it to zero -> unreliable
gyroscope_scale = np.array([0.0, 0.0, 0.0])

# File paths
file1_path = r"Assingment 1B data\imu_417.csv"
file2_path = r"Assingment 1B data\imu_423.csv"
file3_path = r"Assingment 1B data\imu_425.csv"

file_paths = [file1_path, file2_path, file3_path]

# Load IMU data from CSV file
def load_imu_csv(path):
    data = pd.read_csv(path)

    # Get time column
    if "%time" in data.columns:
        time = data["%time"].to_numpy()
    elif "field.header.stamp" in data.columns:
        time = data["field.header.stamp"].to_numpy()
    else:
        time = data.iloc[:, 0].to_numpy()

    # starting time at 0
    time = (time - time[0]) / 1e9

    # Get gyroscope data
    if "field.angular_velocity.x" in data.columns:
        angular_velocity_x = data["field.angular_velocity.x"].to_numpy()
        angular_velocity_y = data["field.angular_velocity.y"].to_numpy()
        angular_velocity_z = data["field.angular_velocity.z"].to_numpy()
    else:
        angular_velocity_x = data["wx"].to_numpy()
        angular_velocity_y = data["wy"].to_numpy()
        angular_velocity_z = data["wz"].to_numpy()

    # Get accelerometer data
    if "field.linear_acceleration.x" in data.columns:
        acceleration_x = data["field.linear_acceleration.x"].to_numpy()
        acceleration_y = data["field.linear_acceleration.y"].to_numpy()
        acceleration_z = data["field.linear_acceleration.z"].to_numpy()
    else:
        acceleration_x = data["ax"].to_numpy()
        acceleration_y = data["ay"].to_numpy()
        acceleration_z = data["az"].to_numpy()

    # Combine into arrays
    angular_velocity = np.vstack([angular_velocity_x, angular_velocity_y, angular_velocity_z]).T
    acceleration = np.vstack([acceleration_x, acceleration_y, acceleration_z]).T

    return time, angular_velocity, acceleration

# Calibrate IMU measurements
def calibrate_imu(angular_velocity_raw, acceleration_raw):
    # Calibrate acceleration: (raw - bias) / (1 + scale)
    acceleration_calibrated = (acceleration_raw - accelerometer_bias) / (1.0 + accelerometer_scale)
    # Calibrate angular velocity: (raw - bias) / (1 + scale)
    angular_velocity_calibrated = (angular_velocity_raw - gyroscope_bias) / (1.0 + gyroscope_scale)
    return angular_velocity_calibrated, acceleration_calibrated

# we calculate the trajectory with constant speed
def calculate_trajectory(time, yaw_rate, speed=1.0):
    number_of_points = len(time)
    heading = np.zeros(number_of_points)
    position_x = np.zeros(number_of_points)
    position_y = np.zeros(number_of_points)

    for i in range(1, number_of_points):
        time_step = time[i] - time[i-1]

        if time_step <= 0:
            heading[i] = heading[i-1]
            position_x[i] = position_x[i-1]
            position_y[i] = position_y[i-1]
            continue

        # Update heading so integrate yaw rate
        heading[i] = heading[i-1] + yaw_rate[i] * time_step
        # Update position
        position_x[i] = position_x[i-1] + speed * np.cos(heading[i]) * time_step
        position_y[i] = position_y[i-1] + speed * np.sin(heading[i]) * time_step

    return position_x, position_y, heading

# we calculate the trajectory with acceleration integration
def calculate_trajectory_with_acceleration(time, yaw_rate, acceleration_body):
    number_of_points = len(time)
    heading = np.zeros(number_of_points)
    velocity_x = np.zeros(number_of_points)
    velocity_y = np.zeros(number_of_points)
    position_x = np.zeros(number_of_points)
    position_y = np.zeros(number_of_points)

    # starting velocity is 1 m/s in x direction
    velocity_x[0] = 1.0
    velocity_y[0] = 0.0


    for i in range(1, number_of_points):
        time_step = time[i] - time[i-1]

        if time_step <= 0:
            heading[i] = heading[i-1]
            velocity_x[i] = velocity_x[i-1]
            velocity_y[i] = velocity_y[i-1]
            position_x[i] = position_x[i-1]
            position_y[i] = position_y[i-1]
            continue

        # Update heading so integrate yaw rate
        heading[i] = heading[i-1] + yaw_rate[i] * time_step

        # Rotate acceleration from body frame to navigation frame
        cos_heading = np.cos(heading[i])
        sin_heading = np.sin(heading[i])
        acceleration_nav_x = cos_heading * acceleration_body[i, 0] - sin_heading * acceleration_body[i, 1]
        acceleration_nav_y = sin_heading * acceleration_body[i, 0] + cos_heading * acceleration_body[i, 1]

        # Update velocity by integrating acceleration
        velocity_x[i] = velocity_x[i-1] + acceleration_nav_x * time_step
        velocity_y[i] = velocity_y[i-1] + acceleration_nav_y * time_step

        # Update position by integrating velocity
        position_x[i] = position_x[i-1] + velocity_x[i] * time_step
        position_y[i] = position_y[i-1] + velocity_y[i] * time_step

    return position_x, position_y, heading

# Calculate drift distance
def calculate_drift(position_x, position_y):
    drift = np.sqrt((position_x[-1] - position_x[0])**2 + (position_y[-1] - position_y[0])**2)
    return drift

# Plot trajectory
def plot_trajectory(position_x, position_y, title):
    plt.figure()
    plt.plot(position_x, position_y, linestyle='--', marker='o', color='b', label='line with marker')
    plt.axis("equal")
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    plt.title(title)
    plt.grid(True)
# Process one file
def process_file(csv_path):
    # Load data
    time, angular_velocity_raw, acceleration_raw = load_imu_csv(csv_path)

    # Calibrate data
    angular_velocity_calibrated, acceleration_calibrated = calibrate_imu(angular_velocity_raw, acceleration_raw)

    # Calculate trajectories using yaw rate and constant speed
    yaw_rate_calibrated = angular_velocity_calibrated[:, 2]
    yaw_rate_raw = angular_velocity_raw[:, 2]

    position_x_calibrated, position_y_calibrated, heading_calibrated = calculate_trajectory(time, yaw_rate_calibrated, speed=1.0)
    position_x_raw, position_y_raw, heading_raw = calculate_trajectory(time, yaw_rate_raw, speed=1.0)

    # Calculate the drift for constant speed method
    drift_calibrated = calculate_drift(position_x_calibrated, position_y_calibrated)
    drift_raw = calculate_drift(position_x_raw, position_y_raw)

    # Calculate trajectories using acceleration integration
    position_x_accel_calibrated, position_y_accel_calibrated, heading_accel_calibrated = calculate_trajectory_with_acceleration(time, yaw_rate_calibrated, acceleration_calibrated)
    position_x_accel_raw, position_y_accel_raw, heading_accel_raw = calculate_trajectory_with_acceleration(time, yaw_rate_raw, acceleration_raw)

    # Calculate the drift for acceleration method
    drift_accel_calibrated = calculate_drift(position_x_accel_calibrated, position_y_accel_calibrated)
    drift_accel_raw = calculate_drift(position_x_accel_raw, position_y_accel_raw)

    # results
    print(f"\nFile: {csv_path}")
    print(f"Constant speed method:")
    print(f"  Drift with calibration:    {drift_calibrated:.4f} m")
    print(f"  Drift without calibration: {drift_raw:.4f} m")
    print(f"Acceleration integration method:")
    print(f"  Drift with calibration:    {drift_accel_calibrated:.4f} m")
    print(f"  Drift without calibration: {drift_accel_raw:.4f} m")

    # plotting trajectories for constant speed method
    plot_trajectory(position_x_calibrated, position_y_calibrated, "Constant speed - with IMU calibration")
    plot_trajectory(position_x_raw, position_y_raw, "Constant speed - without IMU calibration")

    # plotting trajectories for acceleration integration method
    plot_trajectory(position_x_accel_calibrated, position_y_accel_calibrated, "Acceleration integration - with IMU calibration")
    plot_trajectory(position_x_accel_raw, position_y_accel_raw, "Acceleration integration - without IMU calibration")

    return drift_calibrated, drift_raw, drift_accel_calibrated, drift_accel_raw

# Process all files
for file_path in file_paths:
    process_file(file_path)

plt.show()
