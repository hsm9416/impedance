import pickle

def load_robot_state():
    with open('robot_state_log.pkl', 'rb') as f:
        robot_state_log = pickle.load(f)
    return robot_state_log

if __name__ == '__main__':
    robot_state_data = load_robot_state()
    # 리스트를 정의하려면 먼저 빈 리스트를 만들어야 합니다.
    split_data = []  # 빈 리스트로 시작
    for data in robot_state_data:  # 각 요소에 대해 반복
        split_data.append(data)  # 현재 요소를 split_data에 추가

        # 첫 번째 요소만 출력하려면 루프 바깥에서 한 번만 출력해야 합니다.
    print(split_data[0])
    print(split_data[1])
    print(split_data[2])
    print(split_data[3])
    print(split_data[4])
    print(split_data[5])
    print(split_data[6])
    print(split_data[7]) 