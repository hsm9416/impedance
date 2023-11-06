import time

def gait_cycle():
    total_duration = 2  # 총 지속 시간 (초)
    max_value = 100  # 최대 값
    sleep_time = total_duration / max_value  # 각 숫자당 지연 시간 계산

    for i in range(max_value + 1):
        yield i  # 현재 숫자를 반환
        time.sleep(sleep_time)  # 설정된 지연 시간만큼 대기

if __name__ == '__main__':
    while True:
        for current_value in gait_cycle():
            print(current_value)
