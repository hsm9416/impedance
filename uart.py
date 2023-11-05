import serial
import time
import test

# 시리얼 객체 생성
def main():

    try:
        with serial.Serial(
            port="/dev/ttyTHS0",
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            stopbits=serial.STOPBITS_ONE
        ) as ser:
            command_1 = "\r\nTOGGLE#1\r\n".encode()  # 문자열을 바이트로 인코딩
            ser.write(command_1)
            
            print("Command sent")

            # 데이터 읽기
            while True:
                start_time = time.time()
                data = ser.readline().decode('utf-8', errors="ignore").strip()  # 데이터 읽고, 디코딩
                # 데이터가 비어있지 않으면 출력
                split_data = data.split('|')
                Robot_time = split_data[0]
                l_hip_angle = float(split_data[1])
                r_hip_angle = float(split_data[2])
                l_hip_velocity = float(split_data[3])
                r_hip_velocity = float(split_data[4])
                l_hip_current = float(split_data[5])
                r_hip_current = float(split_data[6])
                contorl_mode = split_data[9]
                control_interval = split_data[10]

                
                desired_angle = 0
                desired_velocity = 0
                mass = 1
                stiffness = 1
                damping = 1

                l_controller = test.ImpedanceControl(mass,stiffness,damping)
                r_controller = test.ImpedanceControl(mass,stiffness,damping)

             # 명령 생성 및 전송
                try:
                    # l_tau = l_controller.impedance_control(desired_angle,desired_velocity,l_hip_angle,l_hip_velocity)
                    l_tau = 200
                    r_tau = -200
                    limit_l_tau = test.angle_limit(l_hip_angle,l_tau)
                    l_command = test.send_left_command(limit_l_tau)
                    ser.write(l_command)

                    # r_tau = r_controller.impedance_control(desired_angle,desired_velocity,r_hip_angle,r_hip_velocity)
                    limit_r_tau = test.angle_limit(r_hip_angle,r_tau)
                    r_command = test.send_right_command(limit_r_tau)
                    ser.write(r_command)

                    l_controller.update_state(l_hip_angle,l_hip_velocity)
                    r_controller.update_state(r_hip_angle,r_hip_velocity)
                    # time.sleep(0.05)
  
                    

                except serial.SerialException as e:
                    print(f"Serial communication error: {e}")
                    break
                

                print(f"l_hip_angle: {l_hip_angle}")
                print(f"r_hip_angle: {r_hip_angle}")
                print(f"l_tau: {l_tau}")
                print(f"r_tau: {r_tau}")
                print(f"l_hip_current: {l_hip_current}")
                print(f"r_hip_current: {r_hip_current}")
                print(f"contorl_mode: {contorl_mode}")
                print(f"control_interval: {control_interval}")
                print(f"elapsed_time: {}")




    except KeyboardInterrupt:
        print("Manual interrupt received, stopping...")
    finally:
        print("Program ended.")

if __name__ == "__main__":
    main()

