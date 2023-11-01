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
class ImpedanceController:
    def __init__(self, mass, damping, stiffness):
        """
        Initialize the 1-DoF Impedance Controller with the given parameters.

        :param mass: Mass of the system (m)
        :param damping: Damping coefficient (b)
        :param stiffness: Stiffness coefficient (k)
        """
        self.mass = mass
        self.damping = damping
        self.stiffness = stiffness
        self.position = 0
        self.velocity = 0
        self.force = 0

    def update(self, desired_position, actual_position, actual_velocity, dt):
        """
        Update the controller state based on the desired position, actual position,
        actual velocity, and time step.

        :param desired_position: Desired position (setpoint)
        :param actual_position: Current position of the system
        :param actual_velocity: Current velocity of the system
        :param dt: Time step for the update
        :return: Commanded force to apply to the system
        """
        position_error = desired_position - actual_position
        self.force = (self.stiffness * position_error - 
                      self.damping * actual_velocity)
        self.update_state(dt)
        return self.force

    def update_state(self, dt):
        """
        Update the internal state of the system (position and velocity) based on
        the applied force and time step.

        :param dt: Time step for the update
        """
        acceleration = self.force / self.mass
        self.velocity += acceleration * dt
        self.position += self.velocity * dt



def send_left_command(l_tau):
    l_command = f"\r\nCURRENT?L#{l_tau}|".encode()
    ser.write(l_command)
    return l_command

def send_right_command(r_tau):
    r_command = f"\r\nCURRENT?R#{r_tau}|".encode()
    ser.write(r_command)
    return r_command

l_controller = ImpedanceController(1, 1, 1)
l_desired_position = 0
l_actual_position = uart.l_hip_angle
l_actual_velocity = uart.l_hip_velocity
dt = 0.01
l_tau = l_controller.update(l_desired_position, l_actual_position, l_actual_velocity, dt)
l_controller.update_state(dt)

r_controller = ImpedanceController(1, 1, 1)
r_desired_position = 0
r_actual_position = uart.r_hip_angle
r_actual_velocity = uart.r_hip_velocity
dt = 0.01
r_tau = r_controller.update(r_desired_position, r_actual_position, r_actual_velocity, dt)
r_controller.update_state(dt)
try:
    # 사용자로부터 입력받기
    user_input = input("Enter '1' to send the command: ")

    while True:   # 사용자가 '1'을 입력하면 명령 전송
        if user_input == '1':
            
            r_tau = -150
            l_command = send_left_command(l_tau)
            r_command = send_right_command(r_tau)
            ser.write(l_command)
            ser.write(r_command)
            print('===============================')
            # time.sleep(0.5) 

except KeyboardInterrupt:
    l_tau = 0
    r_tau = 0
    l_command = send_left_command(l_tau)
    r_command = send_right_command(r_tau)
    ser.write(l_command)
    ser.write(l_command)
    print("stopped")
    time.sleep(0.5) 
    print("\nProgram terminated by user.")
finally:
    ser.close()  # 시리얼 포트 닫기
    print("Serial port closed.")
 