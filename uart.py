
import serial
import time

# 시리얼 객체 생성
ser = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)

try:
        command = "\r\nTOGGLE#1\r\n".encode()  # 문자열을 바이트로 인코딩
        ser.write(command)
        print("Command sent, waiting for response...")
        # 데이터 읽기
        while True:
            data = ser.readline().decode('utf-8', errors="ignore").strip()  # 데이터 읽고, 디코딩
            if data:  # 데이터가 비어있지 않으면 출력
                split_data = data.split('|')
                Robot_time,l_hip_angle,r_hip_angle,l_hip_velocity,l_hip_velocity,l_hip_torque,r_hip_torque,l_hip_targetspeed,r_hip_targetspeed,control_mode,control_interval=split_data

                # print(f"Robot_time: {Robot_time}")
                print(f"l_hip_angle: {l_hip_angle}")
                print(f"r_hip_angle: {r_hip_angle}")
                print(f"l_hip_velocity: {l_hip_velocity}")
                print(f"l_hip_velocity: {l_hip_velocity}")
                print(f"l_hip_torque: {l_hip_torque}")
                print(f"r_hip_torque: {r_hip_torque}")
                print("=====================================")

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
finally:
    ser.close()  # 시리얼 포트 닫기
    print("Serial port closed.")
