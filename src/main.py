import cv2
import logging
import numpy as np
import os
import pickle
from CarParkingCounterUtils import CarParkingCounterUtils as utils

logger = logging.getLogger(__name__)


def check_parking_space_availability(processed_img):
    global parking_spaces
    try:
        with open(PARKING_POSITION_FILE_PATH, 'rb') as f:
            parking_spaces = pickle.load(f)
    except FileNotFoundError as err:
        logger.error(err)
        raise

    free_spaces = 0
    for parking_space in parking_spaces:
        x, y = parking_space
        # The above example shows the value at (y, x) = (100, 150), i.e., the 100th row and 150th column of pixels.
        crop_img = processed_img[y:y+utils.RECTANGLE_HEIGHT, x:x+utils.RECTANGLE_WIDTH]
        non_zero_counter = cv2.countNonZero(crop_img)

        if non_zero_counter < 800:
            free_spaces += 1
            utils.rectangle(img=car_parking_img, coordinate=(x, y))
            utils.putText(img=car_parking_img, coordinate=(x, y), text=str(non_zero_counter))
        else:
            utils.rectangle(img=car_parking_img, coordinate=(x, y), rcolor=utils.DEEPPINK_RCOLOR)
            utils.putText(img=car_parking_img, coordinate=(x, y), text=str(non_zero_counter), rcolor=utils.DEEPPINK_RCOLOR)

    free_space_text = f'Free spaces: {free_spaces}/{len(parking_spaces)}'
    utils.putText(img=car_parking_img, coordinate=(50, 20), text=free_space_text, offsets=(7,0,7,0), font_scale=1, rcolor=utils.BLACK_RCOLOR)
    cv2.imshow('car_parking_img', car_parking_img)


def process_image():
    """
    Apply algorithms on original image.
    Algorithms are gray, gussian blur, adaptive threshold, median blur and dilate.

    returns: processed image
    """
    img_gray = cv2.cvtColor(car_parking_img, cv2.COLOR_BGR2GRAY)
    img_blur = cv2.GaussianBlur(img_gray, (3, 3), 1)
    img_threshold = cv2.adaptiveThreshold(img_blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 25, 16)
    img_median = cv2.medianBlur(img_threshold, 5)
    kernel = np.ones((3, 3), np.uint8)
    img_dilate = cv2.dilate(img_median, kernel, iterations=1)

    return img_dilate


if __name__ == '__main__':
    root_dirname = os.path.dirname(os.path.dirname(__file__))
    PARKING_SPACE_VIDEO_FILE_PATH = f'{root_dirname}/src/{utils.PARKING_SPACE_VIDEO_FILENAME}'
    PARKING_POSITION_FILE_PATH = f'{root_dirname}/src/{utils.PARKING_POSITION_FILENAME}'
    parking_spaces = []
    # cv2.VideoCapture(0) means first camera or webcam
    cap = cv2.VideoCapture(PARKING_SPACE_VIDEO_FILE_PATH)

    while True:
        success, car_parking_img = cap.read()

        if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
            # set to the beginning of the video
            # cctv live streaming will not have this issue
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        processed_img = process_image()
        check_parking_space_availability(processed_img)
        key = cv2.waitKey(10)

        # press 'q' to quit the running program, might not be neccessary for cctv
        if key == ord('q'):
            break
