# #################################################
# #############IMPEDANCE CONTROL##################
# #################################################

import serial
import time
import numpy as np
from uart import uart_loop, process_data, read_serial_data
import threading

# 시리얼 객체 생성
ser = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)

class ImpedanceControl:
    
    def __init__(self,mass,stiffness,damping):
        self.mass = mass
        self.stiffness = stiffness
        self.damping = damping
    
    def impedance_control(self,desired_angle,desired_velocity,angle,velocity):
        tau = self.stiffness*(desired_angle-angle) + self.damping*(desired_velocity-velocity)
        return tau

    def update_state(self,angle,velocity):
        self.angle = angle
        self.velocity = velocity

def angle_limit(angle,tau):
    if angle > 60:
        tau = 0
    elif angle < -60:
        tau = 0
    return tau

def send_left_command(l_tau):
    l_command = f"\r\nCURRENT?L#{l_tau}|".encode()
    ser.write(l_command)  # ser 객체를 전역에서 참조

def send_right_command(r_tau):
    r_command = f"\r\nCURRENT?R#{r_tau}|".encode()
    ser.write(r_command)  # ser 객체를 전역에서 참조
    


class DataProcessingThread(threading.Thread):
    def __init__(self, ser):
        super().__init__(daemon=True)
        self.ser = ser

    def run(self):
        while True:
 
            data = read_serial_data(self.ser)  # 사용자 정의 함수를 호출하여 데이터를 읽습니다.
            if data:
                processed_data = process_data(data)  # 사용자 정의 함수를 호출하여 데이터를 처리합니다.
                if processed_data:
                               
                    Robot_time, l_hip_angle, r_hip_angle, l_hip_velocity, r_hip_velocity, l_hip_torque, r_hip_torque, l_hip_targetspeed, r_hip_targetspeed, control_mode, control_interval = processed_data

                    # 각도 제한을 적용할 수 있습니다. 이 예제에서는 구현되지 않았습니다.
                    l_hip = angle_limit(l_hip_angle, l_hip_torque)
                    r_hip = angle_limit(r_hip_angle, r_hip_torque)
                    l_hip = l_hip_angle
                    r_hip = r_hip_angle
                    l_vel = l_hip_velocity
                    r_vel = r_hip_velocity
                    # Impedance control calculations here
                    self.control_left = ImpedanceControl(1,1,1)
                    self.control_right = ImpedanceControl(1,1,1)

                    l_tau = self.control_left.impedance_control(0,0,0,0)  # 현재 상태의 인자를 적절하게 제공해야 합니다.
                    r_tau = self.control_right.impedance_control(0,0,0,0)  # 현재 상태의 인자를 적절하게 제공해야 합니다.

                    self.control_left.update_state(l_hip, l_vel)
                    self.control_right.update_state(r_hip, r_vel)

                    print(f"l_tau : {l_tau}")
                    print(f"r_tau : {r_tau}")
                    print('===============================')

                    
class CommandSendingThread(threading.Thread):
    def __init__(self, ser, control_left, control_right):
        super().__init__(daemon=True)
        self.ser = ser
        self.control_left = control_left
        self.control_right = control_right

    def run(self,l_tau, r_tau):
        while True:

            send_left_command(l_tau)  # 왼쪽 토크 값 전송
            send_right_command(r_tau)  # 오른쪽 토크 값 전송
            time.sleep(0.1)  # 적절한 대기 시간 설정


def main():
    # 시리얼 포트 열기
    if not ser.is_open:
        ser.open()

    # ImpedanceControl 인스턴스 생성
    control_left = ImpedanceControl(1, 1, 1)
    control_right = ImpedanceControl(1, 1, 1)

    # 스레드 생성 및 시작
    data_thread = DataProcessingThread(ser)
    command_thread = CommandSendingThread(ser, control_left, control_right)
    data_thread.start()
    command_thread.start()

    try:
        while True:
            processed_data = uart_loop(ser)
            if processed_data is None:
                print("No data or error in data reception.")
                continue

            data_thread = DataProcessingThread(ser)
            command_thread = CommandSendingThread(ser, control_left, control_right)
            data_thread.start()
            command_thread.start()


    except KeyboardInterrupt:
        send_left_command(0)  # 왼쪽 토크 정지 명령 전송
        send_right_command(0)  # 오른쪽 토크 정지 명령 전송
        print("Program terminated by user.")
        time.sleep(0.5)

    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()



