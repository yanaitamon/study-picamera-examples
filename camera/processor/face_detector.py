from __future__ import print_function
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
import cv2

class FaceDetector(object):
    def __init__(self, flip = True):
        self.vs = PiVideoStream(resolution=(800, 608)).start()
        self.flip = flip
        time.sleep(2.0)

        # opencvの顔分類器(CascadeClassifier)をインスタンス化する
        self.face_cascade = cv2.CascadeClassifier('camera/processor/model/haarcascades/haarcascade_frontalface_default.xml')
        self.eye_cascade = cv2.CascadeClassifier('camera/processor/model/haarcascades/haarcascade_eye.xml')

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        frame = self.process_image(frame)
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()

    def process_image(self, frame):
        # opencvでframe(カラー画像)をグレースケールに変換
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # 上記でグレースケールに変換したものをインスタンス化した顔分類器の
        # detectMultiScaleメソッドで処理し、認識した顔の座標情報を取得する
        faces = self.face_cascade.detectMultiScale(gray, 1.3, 3)

        # 文字列を作成する
        iSize = len(faces)
        # iRow = frame.shape[0]
        # iCol = frame.shape[1]
        font = cv2.FONT_HERSHEY_SIMPLEX

        # 取得した座標情報を元に、cv2.rectangleを使ってframe上に
        # 顔の位置を描画する
        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(128,128,0),2)
            face = frame[y: y + h, x: x + w]
            face_gray = gray[y: y + h, x: x + w]
            eyes = self.eye_cascade.detectMultiScale(face_gray)
            for (ex, ey, ew, eh) in eyes:
                cv2.rectangle(face, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        # 文字列を書く
        cv2.putText(frame,str(iSize),(10,100), font, 4,(128,0,255),3,cv2.LINE_AA)
        # frameを戻り値として返す
        return frame
