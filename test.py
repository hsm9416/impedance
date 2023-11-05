import serial
import time
import numpy as np
import uart

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
    return l_command

def send_right_command(r_tau):
    r_command = f"\r\nCURRENT?R#{r_tau}|".encode()
    return r_command

def main():
    try:
        # 사용자로부터 입력받기
        user_input = input("Enter '1' to send the command: ")
    
        while True:   # 사용자가 '1'을 입력하면 명령 전송
            if user_input == '1':
            
                l_tau = 200
                r_tau = -200
                l_command = send_left_command(l_tau)
                r_command = send_right_command(r_tau)
                ser.write(l_command) 
                ser.write(r_command)
                print(f"l_tau : {l_tau}")
                print(f"r_tau : {r_tau}")
                print('===============================')
    
    except KeyboardInterrupt:
        l_tau = 0
        r_tau = 0
        l_command = send_left_command(l_tau)
        r_command = send_right_command(r_tau)
        command = "\r\nTOGGLE#0\r\n".encode()  # 문자열을 바이트로 인코딩
        ser.write(command)
        ser.write(l_command)
        ser.write(r_command)
        print("stopped")
        time.sleep(0.5) 
        print("\nProgram terminated by user.")
    
    finally:
        ser.close()  # 시리얼 포트 닫기
        print("Serial port closed.")


if __name__ == "__main__":
    main()
 