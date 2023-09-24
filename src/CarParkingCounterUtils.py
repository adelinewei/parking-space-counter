import cv2


class CarParkingCounterUtils:
    # Information of the most top left rectangle:
    # (top_left_x, top_left_y) = (50, 97)
    # (top_right_x, top_right_y) = (155, 143)

    RECTANGLE_WIDTH, RECTANGLE_HEIGHT = 105, 46

    PARKING_POSITION_FILENAME = 'parking_space_position'
    BASE_PARKING_SPACE_FILENAME = 'car_parking_img.png'
    PARKING_SPACE_VIDEO_FILENAME = 'car_parking_video.mp4'

    LIMEGREEN_RCOLOR = (50, 205, 50)        # color for free spaces
    DEEPPINK_RCOLOR = (255, 0, 255)         # color for occupied spaces and picker
    WHITE_RCOLOR = (255, 255, 255)
    BLACK_RCOLOR = (0, 0, 0)

    @staticmethod
    def rectangle(img, coordinate, rcolor=LIMEGREEN_RCOLOR, thickness=2):
        """
        A wrapper of cv2 rectangle for showing a fix-sized rectangle with width 105 and height 46.

        params:
        img: The image to show on
        coordinate: Tuple. Coordinates of the event
        rcolor: RGB color to be filled in rectangle
        thickness: Thickness of the boarder of a rectangle
        """
        x, y = coordinate
        cv2.rectangle(img, (x, y), (x+CarParkingCounterUtils.RECTANGLE_WIDTH, y+CarParkingCounterUtils.RECTANGLE_HEIGHT), rcolor, thickness)

    @staticmethod
    def putText(img, coordinate, text, offsets=(5,0,0,0), font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=0.6, rcolor=LIMEGREEN_RCOLOR, thickness=2):
        """
        A wrapper of cv2 rectangle and cv2 putText for showing text on colored rectangle.
        The default values of arguments are defined based on the most happening case.
        Which means the number of non-zero pixels shown on the bottom left of selected a parking space.

        params:
        img: The image to show on
        x, y: Integers. Coordinates of the event
        text: Text to be shown on the input image
        offsets: Offset of colored rectangle around input text
        font: The font to be shown
        font_scale: The scale of the font
        rcolor: RGB color to be filled in rectangle
        thickness: Thickness of input text ???
        """
        x, y = coordinate
        up_offset, right_offset, down_offset, left_offset = offsets    # offset of height, so that we have a bit of color above the actual text
        (w, h), _ = cv2.getTextSize(text, font, font_scale, thickness)

        x1 = x - left_offset
        y1 = y + CarParkingCounterUtils.RECTANGLE_HEIGHT - h - up_offset
        x2 = x + w + right_offset
        y2 = y + CarParkingCounterUtils.RECTANGLE_HEIGHT + down_offset

        # we get a rectangle filled in with colors if thickness is set to -1
        cv2.rectangle(img, (x1, y1), (x2, y2), rcolor, -1)
        cv2.putText(img, text, (x, y+CarParkingCounterUtils.RECTANGLE_HEIGHT), font, font_scale, CarParkingCounterUtils.WHITE_RCOLOR, thickness)
