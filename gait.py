###############################################################
###################로봇의 초기 데이터 수집 코드#####################
##############################################################


import time
import pickle
from uart import init_serial, uart_loop, toggle

def gait_cycle():
    ser = init_serial()
    toggle()
    total_duration = 2
    max_value = 100
    sleep_time = total_duration / max_value

    # 조건에 맞는 데이터 로깅을 위한 변수 초기화
    combined_logs = []
    save_count = 0  # 저장된 횟수를 추적하는 카운터

    # 최댓값, 최솟값 탐색을 위한 초기 변수 설정
    max_hip_angle_10_20_value = float('-inf')  # 최대 힙 각도 값 초기화 (10-20 범위)
    min_hip_angle_20_60_value = float('inf')  # 최소 힙 각도 값 초기화 (20-60 범위)
    max_hip_angle_60_80_value = float('-inf')  # 최대 힙 각도 값 초기화 (60-80 범위)
    start_value = 0  # Start 값 초기화
    end_value = 0  # End 값 초기화

    for cycle in range(10):  # 10번의 시퀀스를 기록
        for current_value in range(max_value + 1):
            uart_data = uart_loop(ser)

            # 현재 값에 따라 조건별 데이터 로깅
            if current_value == 0:  # Start 포인트
                start_value = float(uart_data[2])  # Start 데이터 기록
                max_hip_angle_10_20_value = float(uart_data[2])  # 최대값 초기화를 현재 값으로 설정
                min_hip_angle_20_60_value = float(uart_data[2])  # 최소값 초기화를 현재 값으로 설정

            elif 0 < current_value <= 20:
                max_hip_angle_10_20_value = max(max_hip_angle_10_20_value, float(uart_data[2]))

            elif 20 < current_value <= 60:
                min_hip_angle_20_60_value = min(min_hip_angle_20_60_value, float(uart_data[2]))

            elif 60 < current_value <= 80:
                max_hip_angle_60_80_value = max(max_hip_angle_60_80_value, float(uart_data[2]))

            elif current_value == 100:  # End 포인트
                end_value = float(uart_data[2])  # End 데이터 기록
                # 현재 시퀀스의 로그를 기록
                combined_logs.append((start_value, max_hip_angle_10_20_value, min_hip_angle_20_60_value, max_hip_angle_60_80_value, end_value))
                start_value = end_value = max_hip_angle_10_20_value = max_hip_angle_60_80_value = 0
                min_hip_angle_20_60_value = float('inf')
                break  # 현재 시퀀스 끝내고 다음 시퀀스로

            # 로봇 상태를 출력하는 함수
            display_robot_state(uart_data, current_value)
            time.sleep(sleep_time)  # 설정된 지연 시간만큼 대기

        save_count += 1  # 저장 횟수를 증가시킴

    # 모든 사이클이 완료된 후, 조건에 맞는 로그를 한 개의 파일로 저장
    with open('robot_state_log.pkl', 'wb') as f:
        pickle.dump(combined_logs, f)

def display_robot_state(uart_data, current_value):
    if uart_data:  # uart_data가 비어있지 않은지 확인
        print("=====================================")
        print(f"gait_cycle: {current_value}, r_hip_angle: {uart_data[3]}")
        # print(f"gait_cycle: {current_value}, r_hip_angle: {uart_data[3]}")


if __name__ == '__main__':
    gait_cycle()  # 이 함수 호출로 프로그램이 시작됨
