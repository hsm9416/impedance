import serial
import time

# 시리얼 객체 생성
ser = serial.Serial(
    port="/dev/ttyTHS0",
    baudrate=115200,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE
)

try:
    # 사용자로부터 입력받기
    user_input = input("Enter '1' to send the command: ")

    # 사용자가 '1'을 입력하면 명령 전송
    if user_input == '1':
        command =  f"\r\nCURRENT?R#{100}|".encode()  # 문자열을 바이트로 인코딩
        ser.write(command)
        print("Command sent, waiting for response...")
        # 데이터 읽기
        while True:
            print(f"============torque => {command}======================")
    
    elif user_input == '0':
        command2 =  f"\r\nCURRENT?R#{0}|".encode()   # 문자열을 바이트로 인코딩
        ser.write(command2)
        print("stopped")

except KeyboardInterrupt:
    print("\nProgram terminated by user.")
finally:
    ser.close()  # 시리얼 포트 닫기
    print("Serial port closed.")
 