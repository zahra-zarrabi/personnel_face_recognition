import cv2
import numpy as np


class Filter:
    def pencil(face):
        frame_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        inv = 255 - frame_gray
        inv = cv2.GaussianBlur(inv, (21, 21), 0)
        out = cv2.divide(frame_gray, 255 - inv, scale=256.0)
        return out

    def blur(face):
        result=cv2.blur(face,(8,8))
        return result

    def my_hsv(face):
        frame_hsv = cv2.cvtColor(face, cv2.COLOR_BGR2HSV)
        return frame_hsv

    def threshold(face):
        frame_gray = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
        # image=255-frame_gray
        _,thresh1=cv2.threshold(frame_gray,30,255,cv2.THRESH_BINARY)
        return thresh1
    def chessboard(face,w,h):
        res_face = cv2.resize(face, (10, 10))
        res_face = cv2.resize(res_face, (w, h))
        return res_face
    def normal(face):
        frame = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
        return frame

# c=Filter
# # image=cv2.imread('im.jpg')
# c.blend