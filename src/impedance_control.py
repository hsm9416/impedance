# #################################################
# #############IMPEDANCE CONTROL##################
# #################################################

import serial
import time
import numpy as np
from gait import Subscriber
from reference import process_sequences
from uart import init_serial,uart_loop
from test import send_left_command, send_right_command

# 시리얼 객체 생성
ser = init_serial()

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

def main():
    if not ser.is_open:
        ser.open()

    subscriber_instance = Subscriber()  # Subscriber 클래스 인스턴스 생성
    subscriber_instance.listener() 

    robot_state_data = load_robot_state('combined_robot_state_logs.pkl')
    sequences = segment_data_into_sequences(robot_state_data)
    max_hip_10_20_cv, min_hip_20_60_cv, max_hip_60_80_cv, max_hip_10_20_value, min_hip_20_60_value, max_hip_60_80_value = process_sequences(sequences)

    impedance_control_left = ImpedanceControl(0,6,5)
    impedance_control_right = ImpedanceControl(0,6,5)

    if current_value == max_hip_10_20_cv :
        desired_angle = max_hip_10_20_value
    elif current_value == min_hip_20_60_cv :
        desired_angle = min_hip_20_60_value
    elif current_value == max_hip_60_80_cv:
        desired_angle = max_hip_60_80_value

    desired_velocity = 0

    try:
        while True: 
            processed_data = uart_loop(ser)
            if processed_data is None:
                print("No data or error in data reception.")
                continue

            # 데이터 처리 및 임피던스 제어 계산
            Robot_time, l_hip_angle, r_hip_angle, l_hip_velocity, r_hip_velocity, l_hip_torque, r_hip_torque, l_hip_targetspeed, r_hip_targetspeed, control_mode, control_interval = processed_data

            # 각도 제한을 적용할 수 있습니다. 이 예제에서는 구현되지 않았습니다.
            l_hip = round(l_hip_angle,2)
            r_hip = round(r_hip_angle,2)
            l_vel = round(l_hip_velocity,2)
            r_vel = round(r_hip_velocity,2)

            l_tau = impedance_control_left.impedance_control(desired_angle,desired_velocity,l_hip,l_vel)
            r_tau = -impedance_control_right.impedance_control(desired_angle,desired_velocity,r_hip,r_vel)

            l_tau_limit_round = round(l_tau,2)
            r_tau_limit_round = round(r_tau,2)

            l_command = send_left_command(l_tau_limit_round)  # 왼쪽 토크 명령 전송
            r_command = send_right_command(r_tau_limit_round)  # 오른쪽 토크 명령 전송
            ser.write(l_command)
            ser.write(r_command)
            # time.sleep(0.01)

            impedance_control_left.update_state(l_hip, l_vel)
            impedance_control_right.update_state(r_hip, r_vel)


            print(Robot_time)
            print(f"l_hip : {l_hip}")
            print(f"r_hip : {r_hip}") 
            print(f"l_tau : {l_tau_limit_round}")
            print(f"r_tau : {r_tau_limit_round}")
            print(f"l_실제 : {l_hip_torque}")
            print(f"r_실제 : {r_hip_torque}")

            print('===============================')

    except KeyboardInterrupt:
        send_left_command(0)  # 왼쪽 토크 정지 명령 전송
        send_right_command(0)  # 오른쪽 토크 정지 명령 전송
        print("Program terminated by user.")
        time.sleep(1)

    finally:
        ser.close()
        print("Serial port closed.")

if __name__ == "__main__":
    main()
