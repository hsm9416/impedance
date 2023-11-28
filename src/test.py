
##############################################################
###### constant, sine wave를 이용한 토크 명령 전송 테스트 code #####
##############################################################


import serial
import time
import numpy as np
import math
from uart import uart_loop, process_data, read_serial_data

# 시리얼 객체 생성
ser = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)
<<<<<<< HEAD
def main(): 
    command =  f"\r\nCURRENT?R#{-200}|".encode()  # 문자열을 바이트로 인코딩
    ser.write(command)
    print("Command sent, waiting for response...")
   
   
   
    # except KeyboardInterrupt:
    #     command =  f"\r\nCURRENT?R#{0}|".encode()  # 문자열을 바이트로 인코딩
    #     ser.write(command)
    #     print("\nProgram terminated by user.")
    # finally:
    #     ser.close()  # 시리얼 포트 닫기
    #     print("Serial port closed.")

if __name__ == '__main__':
=======

class ImpedanceController:
    def __init__(self, mass, damping, stiffness):

        self.mass = mass
        self.damping = damping
        self.stiffness = stiffness
        self.position = 0
        self.velocity = 0
        self.force = 0

    def update(self, desired_position, actual_position, actual_velocity, dt):

        position_error = desired_position - actual_position
        self.force = (self.stiffness * position_error - 
                      self.damping * actual_velocity)
        self.update_state(dt)
        return self.force

    def update_state(self, dt):

        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt



def send_left_command(l_tau):
    l_command = f"\r\nCURRENT?L#{l_tau}|".encode()
    return l_command

def send_right_command(r_tau):
    r_command = f"\r\nCURRENT?R#{r_tau}|".encode()
    return r_command


def send_reset_command():
    l_command = f"\r\nCURRENT?L#-1001|".encode()
    r_command = f"\r\nCURRENT?R#-1001|".encode()
    return l_command,r_command

def main() : 
    try:
        # 사용자로부터 입력받기
        user_input = input("Enter '1' to send the command: ")

        while True:   # 사용자가 '1'을 입력하면 명령 전송
            if user_input == '1':

                # 주파수와 진폭을 정의합니다.
                frequency = 0.01 # 사인파의 주파수 (Hz)
                amplitude = 50  # 사인파의 진폭

                # 현재 시간을 가져와서 사인파 값을 계산합니다.
                current_time = time.time()  # 현재 시간 (초)
                sin_value = math.sin(2 * math.pi * frequency * current_time)  # 사인 함수 값 계산

                # 사인파 값을 토크에 적용합니다.
                # l_tau = amplitude * sin_value +10  # 왼쪽 토크
                # r_tau = -amplitude * sin_value -10  # 오른쪽 토크 (여기서는 같은 값을 사용하지만 필요에 따라 다를 수 있음)

                l_tau = 200
                r_tau = -200
    
                l_command = send_left_command(l_tau)
                r_command = send_right_command(r_tau)
                # l_reset_command,r_reset_command = send_reset_command()


                ser.write(l_command)
                ser.write(r_command)


                time.sleep(0.01)

                print(f"l_tau: {l_command}")
                print(f"r_tau: {r_command}")
                print('===============================')
    

    except KeyboardInterrupt:
        l_zero_command = send_left_command(0)
        r_zero_command = send_right_command(0)
        ser.write(l_zero_command)
        ser.write(r_zero_command)


        print("stopped")
        print("\nProgram terminated by user.")
    finally:
        ser.close()  # 시리얼 포트 닫기
        print("Serial port closed.")
if __name__ == "__main__":
>>>>>>> 1107
    main()
 ₩₩