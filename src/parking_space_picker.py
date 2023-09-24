import cv2
import os
import pickle
from CarParkingCounterUtils import CarParkingCounterUtils as utils


def mouse_clicked_handler(event, x, y, flags, params):
    """
    Record clicks on the image and save to a file in binary format.

    params:
    event: The event that occured
    x, y: Integers. Coordinates of the event
    flags: Any flags reported by setMouseCallback
    params: Any params returned by setMouseCallback
    """
    if event == cv2.EVENT_LBUTTONDOWN:
        # Select parking space by left click
        selected_positions.append((x, y))
    if event == cv2.EVENT_RBUTTONDOWN:
        # remove parking space by right click
        for i, selected_position in enumerate(selected_positions):
            selected_x, selected_y = selected_position
            if (x > selected_x and x < selected_x+utils.RECTANGLE_WIDTH) and (y > selected_y and y < selected_y+utils.RECTANGLE_HEIGHT):
                del selected_positions[i]

    try:
        with open(PARKING_POSITION_FILE_PATH, 'wb') as f:
            pickle.dump(selected_positions, f)
    except FileNotFoundError as err:
        print(err)
        raise


if __name__ == '__main__':
    root_dirname = os.path.dirname(os.path.dirname(__file__))
    PARKING_POSITION_FILE_PATH = f'{root_dirname}/src/{utils.PARKING_POSITION_FILENAME}'
    BASE_PARKING_SPACE_FILE_PATH = f'{root_dirname}/src/{utils.BASE_PARKING_SPACE_FILENAME}'

    try:
        with open(PARKING_POSITION_FILE_PATH, 'rb') as f:
            selected_positions = pickle.load(f)
    except FileNotFoundError as err:
        print(err)
        selected_positions = []

    while True:
        car_parking_img = cv2.imread(BASE_PARKING_SPACE_FILE_PATH)
        for selected_position in selected_positions:
            x, y = selected_position
            utils.rectangle(car_parking_img, (x, y), rcolor=utils.DEEPPINK_RCOLOR)

        cv2.imshow('car_parking_img', car_parking_img)
        cv2.setMouseCallback('car_parking_img', mouse_clicked_handler)
        key = cv2.waitKey(1)

        # press 'q' to quit parking space picker
        if key == ord('q'):
            break
