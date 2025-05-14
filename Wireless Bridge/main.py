import socket
import time
import json
import serial
import struct

# Configuration
HOST = '127.0.0.1'    # Local host
PORT = 5065           # Port used in Unity script
SERIAL_PORT = 'COM4'  # Serial port where your device is connected
BAUDRATE = 921600     # Updated for binary packet

# Map flex sensor values to finger angles
def map_flex_to_angle(flex_value, flex_min=0, flex_max=1023, angle_min=0, angle_max=45, flex_name=None):
    # Empirical min/max per sensor
    if flex_name == 'Flex0':
        flex_min, flex_max = 1700, 2570
    elif flex_name in ('Flex1', 'Flex2'):
        flex_min, flex_max = 1700, 2500

    flex_value = max(flex_min, min(flex_value, flex_max))
    angle = angle_min + (flex_value - flex_min) * (angle_max - angle_min) / (flex_max - flex_min)
    return angle

# Connect to Unity
def connect_to_unity():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    while True:
        try:
            print(f"Connecting to Unity at {HOST}:{PORT}…")
            sock.connect((HOST, PORT))
            print("✔ Connected to Unity")
            return sock
        except ConnectionRefusedError:
            print("✖ Connection refused, retrying in 5s…")
            time.sleep(5)

# Connect to serial device
def connect_to_serial(port=SERIAL_PORT, baudrate=BAUDRATE):
    try:
        ser = serial.Serial(port, baudrate, timeout=1)
        print(f"✔ Connected to {port} @ {baudrate} baud")
        return ser
    except serial.SerialException as e:
        print(f"✖ Serial error: {e}")
        return None

# Process binary packets and send JSON to Unity
def process_serial_data(sock, ser):
    flex_to_finger = {
        'Flex0': 'Index',
        'Flex1': 'Middle',
        'Flex2': 'Ring'
    }
    extra_fingers = ['Thumb', 'Pinky']
    PACKET_SIZE = 35             # 4 B timestamp + 3×2 B flex + 1 B dataReady + 6×4 B floats
    STRUCT_FMT = '<I3hB6f'       # LE: uint32, int16×3, uint8, float×6

    print("▶ Reading binary packets. Ctrl+C to stop.")
    try:
        while True:
            data = ser.read(PACKET_SIZE)
            if len(data) != PACKET_SIZE:
                continue

            # Unpack sensor packet
            ts, f0, f1, f2, ready, ax, ay, az, gx, gy, gz = struct.unpack(STRUCT_FMT, data)
            # Build dict if you need raw values
            # sensor_data = {'timestamp':ts,'flex0':f0,'flex1':f1,'flex2':f2,'dataReady':ready,
            #                'acc':[ax,ay,az],'gyro':[gx,gy,gz]}

            # — IMU packet —
            imu_msg = {
                "type": "imu",
                "accel": [ax, ay, az],
                "gyro": [gx, gy, gz],
                # "type": "imu"
            }
            sock.sendall((json.dumps(imu_msg) + "\n").encode('utf-8'))
            print(f"Sent IMU: {imu_msg}")

            # — Flex packets —
            flex_vals = {'Flex0': f0, 'Flex1': f1, 'Flex2': f2}
            print(flex_vals)

            # time.sleep(0.1)
            # Send measured fingers
            for flex_name, raw in flex_vals.items():
                finger = flex_to_finger[flex_name]
                angle = map_flex_to_angle(raw, flex_name=flex_name)
                pkt = {"hand": "Left", "finger": finger, "angle": angle}
                sock.sendall((json.dumps(pkt) + "\n").encode('utf-8'))
                print(f"Sent {finger}: {angle:.1f}°")

            # Estimate ring & pinky off Flex2
            mid_ang = map_flex_to_angle(f2, flex_name='Flex2')
            for finger, factor in (('Ring', 0.95), ('Pinky', 1.1)):
                pkt = {"hand": "Left", "finger": finger, "angle": mid_ang * factor}
                sock.sendall((json.dumps(pkt) + "\n").encode('utf-8'))
                print(f"Sent (est.) {finger}: {pkt['angle']:.1f}°")

    except KeyboardInterrupt:
        print("\n■ Stopped by user")
    except Exception as e:
        print(f"⚠ Error: {e}")

if __name__ == "__main__":
    sock = None
    ser = None
    try:
        sock = connect_to_unity()
        ser = connect_to_serial()
        if not ser:
            raise SystemExit
        process_serial_data(sock, ser)
    finally:
        if ser:
            ser.close()
            print("Serial closed")
        if sock:
            sock.close()
            print("Unity socket closed")
