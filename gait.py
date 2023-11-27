import time
import pickle
from uart import init_serial, uart_loop, toggle

def gait_cycle():
    ser = init_serial()
    toggle()
    total_duration = 2
    max_value = 100
    sleep_time = total_duration / max_value

    combined_logs = []

    for cycle in range(10):
        # 초기값 설정
        max_hip_angle_10_20_value = float('-inf')
        min_hip_angle_20_60_value = float('inf')
        max_hip_angle_60_80_value = float('-inf')
        max_hip_10_20_cv = 0
        min_hip_20_60_cv = 0
        max_hip_60_80_cv = 0

        for current_value in range(max_value + 1):
            uart_data = uart_loop(ser)

            # 최대 및 최소값 계산 및 해당 current_value 저장
            if 0 <= current_value <= 20:
                if float(uart_data[2]) > max_hip_angle_10_20_value:
                    max_hip_angle_10_20_value = float(uart_data[2])
                    max_hip_10_20_cv = current_value

            elif 20 < current_value <= 60:
                if float(uart_data[2]) < min_hip_angle_20_60_value:
                    min_hip_angle_20_60_value = float(uart_data[2])
                    min_hip_20_60_cv = current_value

            elif 60 < current_value <= 80:
                if float(uart_data[2]) > max_hip_angle_60_80_value:
                    max_hip_angle_60_80_value = float(uart_data[2])
                    max_hip_60_80_cv = current_value

            display_robot_state(uart_data, current_value)
            time.sleep(sleep_time)

        # 각 사이클의 결과를 combined_logs에 저장
        combined_logs.append((max_hip_10_20_cv, max_hip_angle_10_20_value, min_hip_20_60_cv, min_hip_angle_20_60_value, max_hip_60_80_cv, max_hip_angle_60_80_value))

    with open('combined_robot_state_logs.pkl', 'wb') as f:
        pickle.dump(combined_logs, f)

    return combined_logs

def display_robot_state(uart_data, current_value):
    if uart_data:
        print("=====================================")
        print(f"gait_cycle: {current_value}, r_hip_angle: {uart_data[2]}")

if __name__ == '__main__':
    cycle_logs = gait_cycle()
    for log in cycle_logs:
        print(log)
