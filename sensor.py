import serial


def read_sensor_data():
    while True:
        try:
            # Replace 'COM7' with your actual COM port
            ser = serial.Serial('COM7', 9600, timeout=1)
            data = ser.readline().decode('utf-8').split()
            data = list(data)
            print(data)
            ser.close()

            print(f"Raw data from sensor: '{data}'")  # Debugging print

            try:
                sensor_data = int(data[0])
                sen=data[1]
                print(f"Sensor data: {sensor_data}")
                print(type(sensor_data))
            except ValueError:
                print("Error: Invalid sensor data format")
                break
        except serial.SerialException as e:
            print(f"Error: Could not open port: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")


read_sensor_data()


# def read_ultrasonic_data():
#     try:
#         # Replace 'COM7' with your actual COM port
#         ser = serial.Serial('COM7', 9600, timeout=1)
#         time.sleep(2)  # Delay to ensure the port is ready
#
#         while True:
#             data = ser.readline().decode('utf-8').strip()
#             if data:
#                 try:
#                     distance = float(data)
#                     print(f"Ultrasonic Sensor Distance: {distance} cm")
#                 except ValueError:
#                     print("Error: Invalid sensor data format")
#     except serial.SerialException as e:
#         print(f"Error: Could not open port: {e}")
#     except Exception as e:
#         print(f"An unexpected error occurred: {e}")
#     finally:
#         ser.close()
#
#
# read_ultrasonic_data()
