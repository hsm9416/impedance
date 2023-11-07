# read_data.py 파일

import serial

# 시리얼 객체 생성 및 데이터 읽기 함수
def read_serial_data(ser):
    data = ser.readline().decode('utf-8', errors="ignore").strip()
    return data

# 데이터 처리 함수
def process_data(data):
    split_data = data.split('|')
    if len(split_data) == 11:  # 데이터가 올바르게 split되었는지 확인
        return split_data  # 리스트로 반환
    else:
        raise ValueError("Received data does not match expected format")

# 시리얼 포트 초기화 및 오픈
def toggle():
    ser = init_serial()
    command = "\r\nTOGGLE#1\r\n".encode()  # 문자열을 바이트로 인코딩
    ser.write(command)

def init_serial():
    return serial.Serial(
        port="/dev/ttyTHS0",
        baudrate=115200,
        bytesize=serial.EIGHTBITS,
        parity=serial.PARITY_NONE,
        stopbits=serial.STOPBITS_ONE
    )



# 메인 데이터 읽기 및 처리 루프
def uart_loop(ser):
    try: 
        while True:
            data = read_serial_data(ser)
            if data:  # 데이터가 비어있지 않으면
                # 데이터 처리
                return process_data(data)
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        ser.close()
        print("Serial port closed.")

if __name__ == '__main__':
    ser = init_serial()
    while True:
        processed_data = uart_loop(ser)  # 데이터 처리 루프 실행
        # 변수 할당
        Robot_time, l_hip_angle, r_hip_angle, l_hip_velocity1, l_hip_velocity2, l_hip_torque, r_hip_torque, l_hip_targetspeed, r_hip_targetspeed, control_mode, control_interval = processed_data
        print("data sent")
