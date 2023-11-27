
# ##############################################################
# ############## 시리얼 통신을 통해 데이터를 받아오는 코드 #############
# #############################################################

import serial
import threading
import time

# 시리얼 포트로부터 데이터를 읽어오는 스레드
class SerialReaderThread(threading.Thread):
    def __init__(self, ser):
        threading.Thread.__init__(self)
        self.ser = ser
        self.running = True

    def run(self):
        while self.running:
            time.sleep(0.01)  # 1초 대기
            data = self.ser.readline().decode('utf-8', errors="ignore").strip()
            if data:  # 데이터가 비어있지 않으면 처리
                split_data = data.split('|')
                if len(split_data) == 11:
                    (Robot_time, l_hip_angle, r_hip_angle, l_hip_velocity, r_hip_velocity,
                     l_hip_torque, r_hip_torque, l_hip_targetspeed, r_hip_targetspeed, 
                     control_mode, control_interval) = split_data

                    # 데이터 출력
                    print(f"Robot_time: {Robot_time}")
                    print(f"l_hip_angle: {l_hip_angle}")
                    print(f"r_hip_angle: {r_hip_angle}")
                    print(f"l_hip_velocity: {l_hip_velocity}")
                    print(f"r_hip_velocity: {r_hip_velocity}")
                    print(f"l_hip_current: {l_hip_torque}")
                    print(f"r_hip_current: {r_hip_torque}")
                    print(f"l_hip_targetspeed: {l_hip_targetspeed}")
                    print(f"r_hip_targetspeed: {r_hip_targetspeed}")
                    print(f"control_mode: {control_mode}")
                    print(f"control_interval: {control_interval}")
                    print("=====================================")

    def stop(self):
        self.running = False

# 시리얼 객체 생성
ser = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)

# 시리얼 읽기 스레드 시작
reader_thread = SerialReaderThread(ser)
reader_thread.start()
try:
    while True:
        command = "\r\nTOGGLE#1\r\n".encode()  # 문자열을 바이트로 인코딩
        ser.write(command)
        print("Command sent, waiting for response...")
        time.sleep(5)  # 5초 마다 명령어 전송

except KeyboardInterrupt:
    print("\nProgram terminated by user.")

finally:
    # 스레드 정지 및 자원 정리
    reader_thread.stop()
    reader_thread.join()
    ser.close()  # 시리얼 포트 닫기
    print("Serial port closed.")

###############################################################