import pickle

# Data loading function
def load_robot_state(filepath):
    with open(filepath, 'rb') as f:
        robot_state_log = pickle.load(f)
    return robot_state_log

# Function to segment data into sequences based on the provided structure
def segment_data_into_sequences(data):
    return data

# Function to process sequences and extract required values
def process_sequences(sequences):
    max_hip_10_20_cvs = []
    min_hip_20_60_cvs = []
    max_hip_60_80_cvs = []
    max_hip_10_20_values = []  # Store max values of hip angles between 10-20
    min_20_60_values = []  # Store min values of hip angles between 20-60
    max_hip_60_80_values = []  # Store max values of hip angles between 60-80

    for sequence in sequences:
        argmax_hip_10_20_cv,argmax_hip_20_60_cv,argmax_hip_60_80_cv,max_hip_10_20, min_20_60, max_hip_60_80 = sequence

        # averages.append((start_avg + end_avg) / 2)
        max_hip_10_20_cvs.append(argmax_hip_10_20_cv)
        min_hip_20_60_cvs.append(argmax_hip_20_60_cv)
        max_hip_60_80_cvs.append(argmax_hip_60_80_cv)
        max_hip_10_20_values.append(max_hip_10_20)
        min_20_60_values.append(min_20_60)
        max_hip_60_80_values.append(max_hip_60_80)

    return argmax_hip_10_20_cv,argmax_hip_20_60_cv,argmax_hip_60_80_cv,max_hip_10_20,min_20_60,max_hip_60_80

if __name__ == '__main__':
    robot_state_data = load_robot_state('robot_state_log.pkl')
    sequences = segment_data_into_sequences(robot_state_data)
    argmax_hip_10_20_cvs,argmax_hip_20_60_cvs,argmax_hip_60_80_cvs,max_hip_10_20_values, min_20_60_values, max_hip_60_80_values = process_sequences(sequences)

    print("Maximum 'max_hip_10_20':", max(argmax_hip_10_20_cvs))
    print("Maximum 'max_hip_10_20':", max(argmax_hip_20_60_cvs))
    print("Maximum 'max_hip_10_20':", max(argmax_hip_60_80_cvs))
    print("Maximum 'max_hip_10_20':", max(max_hip_10_20_values))
    print("Minimum 'min_20_60':", min(min_20_60_values))
    print("Maximum 'max_hip_60_80':", max(max_hip_60_80_values))


