#################################################
#############IMPEDANCE CONTROL##################
#################################################

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

def main():
    if not ser.is_open:
        ser.open()

    impedance_control_left = ImpedanceControl(1,1,1)
    impedance_control_right = ImpedanceControl(1,1,1)

    try:
        while True:
            processed_data = uart_loop(ser)
            if processed_data is None:
                print("No data or error in data reception.")
                continue

            # 데이터 처리 및 임피던스 제어 계산
            Robot_time, l_hip_angle, r_hip_angle, l_hip_velocity, r_hip_velocity, l_hip_torque, r_hip_torque, l_hip_targetspeed, r_hip_targetspeed, control_mode, control_interval = processed_data

            # 각도 제한을 적용할 수 있습니다. 이 예제에서는 구현되지 않았습니다.
            # l_hip = angle_limit(l_hip_angle, l_hip_torque)
            # r_hip = angle_limit(r_hip_angle, r_hip_torque)
            l_hip = l_hip_angle
            r_hip = r_hip_angle
            l_vel = l_hip_velocity
            r_vel = r_hip_velocity

            l_tau = impedance_control_left.impedance_control(0,0,l_hip,l_vel)
            r_tau = impedance_control_right.impedance_control(0,0,r_hip,r_vel)

            impedance_control_left.update_state(l_hip, l_vel)
            impedance_control_right.update_state(r_hip, r_vel)

            send_left_command(l_tau)  # 왼쪽 토크 명령 전송
            send_right_command(r_tau)  # 오른쪽 토크 명령 전송

            print(f"l_tau : {l_tau}")
            print(f"r_tau : {r_tau}")
            print('===============================')

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

