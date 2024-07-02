import socket
from threading import Thread
from PIL import ImageFont, ImageDraw, Image
import numpy as np
import cv2
import mediapipe as mp

# 한글을 출력하기 위한 함수
def draw_text(img, text, position, font_size, font_color):
    font_path = "C:/Windows/Fonts/gulim.ttc"  # Windows에서 Gulim 폰트 경로

    # opencv 이미지를 PIL이미지로 변
    
    img_pil = Image.fromarray(img)

    # PIL Draw 객체 생성
    draw = ImageDraw.Draw(img_pil)

    # 폰트 스타일 지정
    font = ImageFont.truetype(font_path, font_size)

    # PIL 이미지에 텍스트 입력
    draw.text(position, text, font=font, fill=font_color)
    return np.array(img_pil) # 최종 numpy array 로 이미지 형태 반환

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

def get_hand_pose(hand_landmarks):
    # 손가락 끝과 PIP(손가락 중간 관절) 사이의 거리를 비교하여 손가락이 펴져 있는지 확인
    open_fingers = []
    for i in [4, 8, 12, 16, 20]:  # 엄지부터 새끼손가락까지의 끝 랜드마크 인덱스
        tip = hand_landmarks.landmark[i]  # 손가락 끝
        pip = hand_landmarks.landmark[i - 2]  # 손가락 중간 관절

        # if handedness.classification[0].label == "Right":  # 오른손인 경우 판별하기

        # 엄지는 x좌표를, 나머지 손가락은 y좌표를 사용하여 개폐 상태 확인 - 오른손 기준
        if i == 4:  # 엄지손가락인 경우
            open_fingers.append(tip.x > pip.x)
        else:
            open_fingers.append(tip.y < pip.y)
    
    if open_fingers.count(True) == 5:
        return "놓기"
    elif open_fingers.count(True) == 0:
        return "잡기"
    else:
        return "모름"


# TCP 서버를 시작하는 함수입니다.
def start_server(host='127.0.0.1', port=65432):
    # socket 객체를 생성합니다. AF_INET은 IPv4를 사용하겠다는 의미이고, SOCK_STREAM은 TCP를 사용하겠다는 의미입니다.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as socket_server:

        # 생성한 소켓을 주어진 호스트와 포트에 바인드(연결)합니다. 이는 서버가 해당 주소에서 클라이언트의 연결을 기다리게 합니다.
        socket_server.bind((host, port))
        
        # 소켓이 클라이언트의 연결을 기다리도록 설정합니다. 이 메서드는 소켓을 "리스닝" 상태로 만듭니다.
        socket_server.listen()
        print(f"서버가 연결되었습니다. {host}:{port}")

        # 클라이언트로부터 연결이 수립되면, accept 메서드는 연결된 클라이언트의 소켓 객체와 주소를 반환합니다.
        conn, addr = socket_server.accept()

        # 클라이언트와 연결된 소켓을 관리하는 코드 블록입니다. 이 블록을 벗어나면 연결은 자동으로 닫힙니다.
        with conn:
            print(f"연결된 소켓은 {addr}")

            while cap.isOpened():
                success, image = cap.read()
                if not success:
                    continue

                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                results = hands.process(image)
                image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

                if results.multi_hand_landmarks:
                    for hand_landmarks in results.multi_hand_landmarks:
                        # 손 랜드마크 그리기
                        mp_drawing.draw_landmarks(
                            image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                            mp_drawing.DrawingSpec(color=(121, 22, 76), thickness=2, circle_radius=4),
                            mp_drawing.DrawingSpec(color=(250, 44, 250), thickness=2))
            
                        # 포즈 판별 및 출력
                        pose = get_hand_pose(hand_landmarks)
            
                        # 한글 출력을 위한 작업
                        image = draw_text(image, pose, (10, 50), 30, (255, 255, 255))

                        data = str(pose).encode()
                        # 받은 데이터를 클라이언트에게 다시 보냅니다. 변형해서 보내도록 수정합니다
                        conn.sendall(data)

                cv2.imshow('Hand Pose', image)

                if cv2.waitKey(5) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()
               

# 이 스크립트가 직접 실행되었을 때만 start_server 함수를 호출합니다.
if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    start_server()



