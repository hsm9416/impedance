# import time
# import pickle
# from uart import init_serial, uart_loop

# ser = init_serial()  # 시리얼 포트 초기화

# def gait_cycle():
#     total_duration = 2 # 총 지속 시간 (초)
#     max_value = 100  # 최대 값
#     sleep_time = total_duration / max_value  # 각 숫자당 지연 시간 계산
#     data_log = []  # 로그 데이터를 저장할 리스트
    
#     while True:  # 무한 루프를 사용하여 실시간으로 계속 데이터를 받음
#         for i in range(max_value + 1):
#             uart_data = uart_loop(ser)  # 시리얼에서 데이터 읽기
#             data_log.append((i, uart_data))  # 현재 값을 로그 리스트에 추가
#             if len(data_log) >= 10:  # 리스트가 10개의 요소를 가질 때마다 파일로 저장
#                 with open('robot_state_log.pkl', 'wb') as f:
#                     pickle.dump(data_log, f)
#                 data_log = []  # 리스트를 비우고 새로 시작
                
#             display_robot_state(uart_data, i)  # 로봇 상태 출력
#             time.sleep(sleep_time)  # 설정된 지연 시간만큼 대기     

# def display_robot_state(uart_data, current_value):
#         if uart_data:  # uart_data가 비어있지 않은지 확인
#             if current_value == 0:
#                 print("=====================================")
#                 print("l_hip_angle: ", uart_data[2])
#             elif current_value == 20:
#                 print("l_hip_angle: ", uart_data[2])
#             elif current_value == 40:
#                 print("l_hip_angle: ", uart_data[2])
#             elif current_value == 60:
#                 print("l_hip_angle: ", uart_data[2])
#             elif current_value == 100:
#                 print("l_hip_angle: ", uart_data[2])
#     # uart_data와 current_value를 기반으로 로봇의 상태를 출력하는 함수
#     # ... (이전에 정의된 코드와 동일)

# if __name__ == '__main__':
#     gait_cycle()  # 이 함수 호출로 프로그램이 시작됨

    #===========================================================================
import time
import pickle
from uart import init_serial, uart_loop ,toggle


ser = init_serial()
send_toggle = toggle()

def gait_cycle():
    send_toggle
    total_duration = 2  # 총 지속 시간 (초)
    max_value = 100  # 최대 값
    sleep_time = total_duration / max_value  # 각 숫자당 지연 시간 계산
    data_log = []  # 로그 데이터를 저장할 리스트
    save_count = 0  # 저장된 횟수를 추적하는 카운터
    
    while save_count < 10:  # 저장 횟수가 10 미만인 동안 계속 실행
        for i in range(max_value + 1):
            uart_data = uart_loop(ser)  # 시리얼에서 데이터 읽기
            data_log.append((i, uart_data))  # 현재 값을 로그 리스트에 추가
            display_robot_state(uart_data, i)  # 로봇 상태 출력
            
            if i == max_value:  # current_value가 100일 때만
                with open('robot_state_log.pkl', 'wb') as f:
                    pickle.dump(data_log, f)
                data_log = []  # 리스트를 비우고 새로 시작
                
            time.sleep(sleep_time)  # 설정된 지연 시간만큼 대기

def display_robot_state(uart_data, current_value):
         if uart_data:  # uart_data가 비어있지 않은지 확인
            if current_value == 0:
                print("=====================================")
            elif current_value == 100:
                print("l_hip_angle: ", uart_data[2])   # uart_data와 current_value를 기반으로 로봇의 상태를 출력하는 함수
    # ... (이전에 정의된 코드와 동일)

if __name__ == '__main__':
    gait_cycle()  # 이 함수 호출로 프로그램이 시작됨
