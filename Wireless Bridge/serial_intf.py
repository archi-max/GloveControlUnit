# import serial
# import re

# def read_from_serial(port='COM4', baudrate=115200):
#     ser = serial.Serial(port, baudrate, timeout=1)
    
#     IMU_FLEX_PATTERN = re.compile(
#         r"Scaled\. Acc \(mg\) \[ (?P<acc_x>[-+]?\d+\.\d+), "
#         r"(?P<acc_y>[-+]?\d+\.\d+), (?P<acc_z>[-+]?\d+\.\d+) \], "
#         r"Gyr \(DPS\) \[ (?P<gyr_x>[-+]?\d+\.\d+), "
#         r"(?P<gyr_y>[-+]?\d+\.\d+), (?P<gyr_z>[-+]?\d+\.\d+) \], "
#         r"Mag \(uT\) \[ (?P<mag_x>[-+]?\d+\.\d+), "
#         r"(?P<mag_y>[-+]?\d+\.\d+), (?P<mag_z>[-+]?\d+\.\d+) \], "
#         r"Tmp \(C\) \[ (?P<tmp>[-+]?\d+\.\d+) \]"
#         r" \| Flex0: (?P<flex0>\d+) \| Flex1: (?P<flex1>\d+) \| Flex2: (?P<flex2>\d+)"
#     )

#     try:
#         while True:
#             line = ser.readline().decode('utf-8', errors='ignore').strip()
#             if not line:
#                 continue

#             print(f"Received line: {line}")
            
#             match = IMU_FLEX_PATTERN.fullmatch(line)
#             if match:
#                 data = match.groupdict()
#                 print("\nFull Dataset:")
#                 print(f"IMU Acc (mg): X={float(data['acc_x']):7.2f}, Y={float(data['acc_y']):7.2f}, Z={float(data['acc_z']):7.2f}")
#                 print(f"IMU Gyr (DPS): X={float(data['gyr_x']):7.2f}, Y={float(data['gyr_y']):7.2f}, Z={float(data['gyr_z']):7.2f}")
#                 print(f"IMU Mag (uT): X={float(data['mag_x']):7.2f}, Y={float(data['mag_y']):7.2f}, Z={float(data['mag_z']):7.2f}")
#                 print(f"IMU Tmp (C): {float(data['tmp']):7.2f}")
#                 print(f"Flex Sensors: [0]: {int(data['flex0']):4d}, [1]: {int(data['flex1']):4d}, [2]: {int(data['flex2']):4d}")
#                 print("-" * 60)
#             else:
#                 # Fallback for partial/broken data
#                 process_flex_data(line)

#     except KeyboardInterrupt:
#         print("Serial reading stopped by user.")
#     finally:
#         ser.close()

# def process_flex_data(line):
#     current_entry = {}
#     flex_found = False
    
#     if 'Flex0:' in line:
#         if (val := re.search(r'Flex0: (\d+)', line)):
#             current_entry['Flex0'] = int(val.group(1))
#             flex_found = True
#     if 'Flex1:' in line:
#         if (val := re.search(r'Flex1: (\d+)', line)):
#             current_entry['Flex1'] = int(val.group(1))
#             flex_found = True
#     if 'Flex2:' in line:
#         if (val := re.search(r'Flex2: (\d+)', line)):
#             current_entry['Flex2'] = int(val.group(1))
#             flex_found = True

#     if flex_found:
#         print(f"Partial flex data: {current_entry}")

# if __name__ == '__main__':
#     read_from_serial()


import serial
import struct
import re
from collections import defaultdict

def read_sensor_data(port='COM4', baudrate=921600):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        try:
            while True:
                data = ser.read(35)  # Match struct size (4+6+1+24=35 bytes)
                if len(data) == 35:
                    unpacked = struct.unpack('<I3hB6f', data)
                    sensor_data = {
                        'timestamp': unpacked[0],
                        'flex0': unpacked[1], 'flex1': unpacked[2], 'flex2': unpacked[3],
                        'dataReady': unpacked[4],
                        'accX': unpacked[5], 'accY': unpacked[6], 'accZ': unpacked[7],
                        'gyrX': unpacked[8], 'gyrY': unpacked[9], 'gyrZ': unpacked[10]
                    }
                    print(sensor_data)
        except KeyboardInterrupt:
            print("Stopped")

if __name__ == '__main__':
    read_sensor_data()
