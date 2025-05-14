import serial

try:
    ser = serial.Serial('COM4', 921600, timeout=1)
    print(f"Port opened: {ser.port} @ {ser.baudrate} baud")
    while True:
        if ser.in_waiting > 0:
            data = ser.readline().decode('utf-8').rstrip()
            print(f"Received: {data}")
except serial.SerialException as e:
    print(f"Error: {e}")
except KeyboardInterrupt:
    print("Stopped by user")
finally:
    if 'ser' in locals() and ser.is_open:
        ser.close()
