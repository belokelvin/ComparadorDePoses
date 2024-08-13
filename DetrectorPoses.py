import cv2, time, math
import mediapipe as mp
import time
import math

class DetectorPoses():
 
    def __init__(self, mode=False, cimaCorpo=False, suavizacao=True,
                 detecContorno=0.7, trackCon=0.7):
 
        self.mode = mode
        self.cimaCorpo = cimaCorpo
        self.suavizacao = suavizacao
        self.detecContorno = detecContorno
        self.trackCon = trackCon
 
        self.mpDraw = mp.solutions.drawing_utils
        self.mpPose = mp.solutions.pose

        self.pose = self.mpPose.Pose(self.mode, min_detection_confidence=detecContorno, min_tracking_confidence=trackCon)
 
    def identificarPose(self, img, draw=True):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        self.results = self.pose.process(imgRGB)
        if self.results.pose_landmarks and draw:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                if id not in [1,2,3,4,5,6,7,8,9,10,17,18,19,20,]:  #Tira as pontos do rosto e dos dedos
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

            # Desenha as conexões menos as do rosto
            for conn in self.mpPose.POSE_CONNECTIONS:
                if conn[0] > 10 and conn[1] > 10:  # Tira conexões envolvendo pontos de referência faciais
                    pt1 = self.results.pose_landmarks.landmark[conn[0]]
                    pt2 = self.results.pose_landmarks.landmark[conn[1]]
                    x1, y1 = int(pt1.x * w), int(pt1.y * h)
                    x2, y2 = int(pt2.x * w), int(pt2.y * h)
                    cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
        return img

 
    def identificarPosicao(self, img, draw=True):
        self.lmList = []
        if self.results.pose_landmarks:
            for id, lm in enumerate(self.results.pose_landmarks.landmark):
                h, w, c = img.shape
                # print(id, lm)
                cx, cy = int(lm.x * w), int(lm.y * h)
                self.lmList.append([id, cx, cy])
                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        return self.lmList
 
    def encontrarAngulo(self, img, p1, p2, p3, draw=True):
 
        # Capturas os pontos
        x1, y1 = self.lmList[p1][1:]
        x2, y2 = self.lmList[p2][1:]
        x3, y3 = self.lmList[p3][1:]
 
        # Angulos
        angulo = math.degrees(math.atan2(y3 - y2, x3 - x2) -
                             math.atan2(y1 - y2, x1 - x2))
        if angulo < 0:
            angulo += 360
  
        # Sesenha no frame
        if draw:
            cv2.line(img, (x1, y1), (x2, y2), (255, 255, 255), 3)
            cv2.line(img, (x3, y3), (x2, y2), (255, 255, 255), 3)
            cv2.circle(img, (x1, y1), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x1, y1), 15, (0, 0, 255), 2)
            cv2.circle(img, (x2, y2), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x2, y2), 15, (0, 0, 255), 2)
            cv2.circle(img, (x3, y3), 10, (0, 0, 255), cv2.FILLED)
            cv2.circle(img, (x3, y3), 15, (0, 0, 255), 2)
            cv2.putText(img, str(int(angulo)), (x2 - 50, y2 + 50),
                        cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 255), 2)
        return angulo

def main():
    cap = cv2.VideoCapture(r'Video_teste/bulgaro_teste.mp4')
    pTempo = 0
    detector = DetectorPoses()
    while True:
        sucesso, img = cap.read()
        img = detector.identificarPose(img)
        lmList = detector.identificarPosicao(img, draw=False)

        lm_to_print = 20
        if len(lmList) != 0:
            print(lmList[lm_to_print])
            cv2.circle(img, (lmList[lm_to_print][1], lmList[lm_to_print][2]), 15, (0, 0, 255), cv2.FILLED)
 
        cTempo = time.time()
        fps = 1 / (cTempo - pTempo)
        pTempo = cTempo
 
        cv2.putText(img, "FPS: "+str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)
 
        cv2.imshow("Image", img)
        cv2.waitKey(1)
 
 
if __name__ == "__main__":
    main()
