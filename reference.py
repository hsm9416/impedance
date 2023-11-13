##############################################################
### Reference Implementation for the Data Processing Module ###
##############################################################

import pickle

# Data loading function
def load_robot_state(filepath):
    with open(filepath, 'rb') as f:  # File path confirmation
        robot_state_log = pickle.load(f)
    return robot_state_log

# Function to segment data into sequences based on the provided structure
def segment_data_into_sequences(data): 
    # Assuming each item in the data list is a complete sequence
    return data  # In this case, no additional processing is needed

# Main execution function
if __name__ == '__main__':
    robot_state_data = load_robot_state('robot_state_log.pkl')  # Load data
    sequences = segment_data_into_sequences(robot_state_data)    # Segment data into sequences
    
    # Now, let's say we need to find the average of 'start' and 'end' values, which are the first and last values in the sequence, and find the maximum 'max_hip_10_20', the minimum 'min_20_60', and the maximum 'max_hip_60_80' which correspond to the second, third, and fourth values respectively.

    averages = []  # Store averages of start and end values
    max_hip_10_20_values = []  # Store max values of hip angles between 10-20
    min_20_60_values = []  # Store min values of hip angles between 20-60
    max_hip_60_80_values = []  # Store max values of hip angles between 60-80
    
    # Iterate over each sequence to calculate the required values
    for sequence in sequences:
        start_avg = sequence[0]
        max_hip_10_20 = sequence[1]
        .0
        min_20_60 = sequence[2]
        max_hip_60_80 = sequence[3]
        end_avg = sequence[4]

        # Calculate the averages and find the max/min as required
        averages.append((start_avg + end_avg) / 2)  # Average of start and end values
        max_hip_10_20_values.append(max_hip_10_20)  # Max value between 10-20
        min_20_60_values.append(min_20_60)          # Min value between 20-60
        max_hip_60_80_values.append(max_hip_60_80)  # Max value between 60-80

    # Print out the calculated values
    print("Maximum 'max_hip_10_20':", max(max_hip_10_20_values))
    print("Minimum 'min_20_60':", min(min_20_60_values))
    print("Maximum 'max_hip_60_80':", max(max_hip_60_80_values))

