import os, sys
sys.path.append(os.path.dirname(os.getcwd()))
from fridgeyocr.fridgeyocr import Reader
import cv2

if __name__ == "__main__":
    reader = Reader()
    image = cv2.imread('/home/guest/speaking_fridgey/fridgeyocr/fridgeyocr/demo/recipt3.jpg')
    reader(image)