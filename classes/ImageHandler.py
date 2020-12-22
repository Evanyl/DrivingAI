import os

IMG_DIR = "imgs"
CAR_NAME = "car.png"


def getCarImgDir():
    return os.path.join(IMG_DIR, CAR_NAME)