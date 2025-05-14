# import socket
# import time
# import json
# import math
# import random

# # Configuration
# HOST = '127.0.0.1'  # Local host
# PORT = 5065         # Port used in Unity script

# # Connect to Unity
# def connect_to_unity():
#     sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#     connected = False
    
#     while not connected:
#         try:
#             print(f"Attempting to connect to Unity at {HOST}:{PORT}...")
#             sock.connect((HOST, PORT))
#             connected = True
#             print("Connected to Unity!")
#         except ConnectionRefusedError:
#             print("Connection refused. Make sure Unity is running and the server is started.")
#             print("Retrying in 5 seconds...")
#             time.sleep(5)
    
#     return sock

# # Simulate realistic finger movement
# def simulate_finger_movement(sock):
#     fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    
#     # Different timing for each finger to make movement look natural
#     phase_shifts = {
#         "Thumb": 0,
#         "Index": 0.5,
#         "Middle": 1.0,
#         "Ring": 1.5,
#         "Pinky": 2.0
#     }
    
#     # Different max angles for each finger
#     max_angles = {
#         "Thumb": 60,
#         "Index": 85,
#         "Middle": 90,
#         "Ring": 80,
#         "Pinky": 75
#     }
    
#     print("Starting finger movement simulation. Press Ctrl+C to stop.")
    
#     try:
#         t = 0
#         while True:
#             for finger in fingers:
#                 # Calculate angle based on sine wave with finger-specific phase and amplitude
#                 # This creates a smooth up-down motion that's offset for each finger
#                 phase = phase_shifts[finger]
#                 max_angle = max_angles[finger]
                
#                 # Sine wave oscillating between 0 and max_angle
#                 angle = (math.sin(t + phase) + 1) / 2 * max_angle
                
#                 # Add small random variations to make movement more natural
#                 angle += random.uniform(-2, 2)
                
#                 # Ensure angle stays within reasonable bounds
#                 angle = max(0, min(angle, max_angle))
                
#                 # Create the data packet
#                 data = {
#                     "hand": "Left",
#                     "finger": finger,
#                     "angle": angle
#                 }
                
#                 # Send to Unity
#                 message = json.dumps(data) + "\n"
#                 sock.sendall(message.encode('utf-8'))
#                 print(f"Sent: {finger} = {angle:.1f} degrees")
            
#             # Small delay to simulate sensor reading frequency
#             time.sleep(0.1)
#             t += 0.05  # Increase time value for next iteration
            
#     except KeyboardInterrupt:
#         print("\nSimulation stopped by user.")
#     finally:
#         sock.close()
#         print("Connection closed.")

# if __name__ == "__main__":
#     try:
#         sock = connect_to_unity()
#         simulate_finger_movement(sock)
#     except Exception as e:
#         print(f"Error: {e}")


import socket
import time
import json
import math
import random
import numpy as np

# Configuration
HOST = '127.0.0.1'  # Local host
PORT = 5065         # Port used in Unity script

def connect_to_unity():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connected = False
    
    while not connected:
        try:
            print(f"Attempting to connect to Unity at {HOST}:{PORT}...")
            sock.connect((HOST, PORT))
            connected = True
            print("Connected to Unity!")
        except ConnectionRefusedError:
            print("Connection refused. Make sure Unity is running and the server is started.")
            print("Retrying in 5 seconds...")
            time.sleep(5)
    
    return sock

def simulate_sensor_data(sock):
    # Finger configuration
    fingers = ["Thumb", "Index", "Middle", "Ring", "Pinky"]
    phase_shifts = {"Thumb": 0, "Index": 0.5, "Middle": 1.0, "Ring": 1.5, "Pinky": 2.0}
    max_angles = {"Thumb": 60, "Index": 85, "Middle": 90, "Ring": 80, "Pinky": 75}

    # IMU simulation parameters
    imu_t = 0
    base_temp = 25.0
    mag_bias = np.random.normal(0, 5, 3)  # Random magnetic bias

    print("Starting sensor simulation. Press Ctrl+C to stop.")
    
    try:
        t = 0
        while True:
            # Simulate finger movements
            finger_data = []
            for finger in fingers:
                phase = phase_shifts[finger]
                max_angle = max_angles[finger]
                angle = (math.sin(t + phase) + 1) / 2 * max_angle
                angle += random.uniform(-2, 2)
                angle = max(0, min(angle, max_angle))
                
                finger_data.append({
                    "type": "finger",
                    "hand": "Left",
                    "finger": finger,
                    "angle": angle
                })

            # Simulate IMU data
            imu_t += 0.02
            accel = [
                math.sin(imu_t) * 500,          # X-axis
                math.cos(imu_t * 0.8) * 300,    # Y-axis 
                (math.sin(imu_t * 0.5) + 1) * 1000  # Z-axis (gravity-like)
            ]
            
            gyro = [
                math.sin(imu_t * 1.2) * 50,
                math.cos(imu_t * 0.9) * 40,
                math.sin(imu_t * 0.7) * 30
            ]
            
            mag = [
                30 + math.sin(imu_t * 0.3) * 5 + mag_bias[0],
                40 + math.cos(imu_t * 0.4) * 5 + mag_bias[1],
                50 + math.sin(imu_t * 0.5) * 5 + mag_bias[2]
            ]
            
            temp = base_temp + math.sin(imu_t * 0.1) * 2

            imu_package = {
                "type": "imu",
                "accel": [round(x, 2) for x in accel],
                "gyro": [round(x, 2) for x in gyro],
                "mag": [round(x, 2) for x in mag],
                "temp": round(temp, 2)
            }

            # Send all data
            for data in finger_data:
                message = json.dumps(data) + "\n"
                sock.sendall(message.encode('utf-8'))
                print(f"Sent finger: {data['finger']} = {data['angle']:.1f}°")
            
            message = json.dumps(imu_package) + "\n"
            sock.sendall(message.encode('utf-8'))
            print(f"Sent IMU: Acc={imu_package['accel']} mg")
            
            # Simulation timing
            time.sleep(0.05)  # 20 Hz update rate
            t += 0.1

    except KeyboardInterrupt:
        print("\nSimulation stopped by user.")
    finally:
        sock.close()
        print("Connection closed.")

if __name__ == "__main__":
    try:
        sock = connect_to_unity()
        simulate_sensor_data(sock)
    except Exception as e:
        print(f"Error: {e}")
