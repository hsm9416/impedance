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
def main(): 
    command =  f"\r\nCURRENT?R#{-200}|".encode()  # 문자열을 바이트로 인코딩
    ser.write(command)
    print("Command sent, waiting for response...")
   
   
   
    # except KeyboardInterrupt:
    #     command =  f"\r\nCURRENT?R#{0}|".encode()  # 문자열을 바이트로 인코딩
    #     ser.write(command)
    #     print("\nProgram terminated by user.")
    # finally:
    #     ser.close()  # 시리얼 포트 닫기
    #     print("Serial port closed.")

if __name__ == '__main__':
    main()
 ₩₩