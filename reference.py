import pickle

# Data loading function
def load_robot_state(filepath):
    with open(filepath, 'rb') as f:
        robot_state_log = pickle.load(f)
    return robot_state_log

# Function to segment data into sequences based on the provided structure
def segment_data_into_sequences(data):
    return data

def process_sequences(sequences):
    max_hip_10_20_cvs = []
    min_hip_20_60_cvs = []
    max_hip_60_80_cvs = []
    max_hip_10_20_values = []
    min_20_60_values = []
    max_hip_60_80_values = []

    for sequence in sequences:
        # sequence를 6개 요소로 언패킹
        max_hip_10_20_cv, max_hip_10_20, min_hip_20_60_cv, min_20_60, max_hip_60_80_cv, max_hip_60_80 = sequence

        max_hip_10_20_values.append(max_hip_10_20)
        max_hip_10_20_cvs.append(max_hip_10_20_cv)

        min_20_60_values.append(min_20_60)
        min_hip_20_60_cvs.append(min_hip_20_60_cv)

        max_hip_60_80_values.append(max_hip_60_80)
        max_hip_60_80_cvs.append(max_hip_60_80_cv)

    return max_hip_10_20_cvs, min_hip_20_60_cvs, max_hip_60_80_cvs, max_hip_10_20_values, min_20_60_values, max_hip_60_80_values

# 메인 코드
if __name__ == '__main__':
    robot_state_data = load_robot_state('combined_robot_state_logs.pkl')
    sequences = segment_data_into_sequences(robot_state_data)
    max_hip_10_20_cvs, min_hip_20_60_cvs, max_hip_60_80_cvs, max_hip_10_20_values, min_20_60_values, max_hip_60_80_values = process_sequences(sequences)

    print("Maximum 'max_hip_10_20_cv':", max(max_hip_10_20_cvs))
    print("Minimum 'min_hip_20_60_cv':", min(min_hip_20_60_cvs))
    print("Maximum 'max_hip_60_80_cv':", max(max_hip_60_80_cvs))
    print("Maximum 'max_hip_10_20':", max(max_hip_10_20_values))
    print("Minimum 'min_20_60':", min(min_20_60_values))
    print("Maximum 'max_hip_60_80':", max(max_hip_60_80_values))





