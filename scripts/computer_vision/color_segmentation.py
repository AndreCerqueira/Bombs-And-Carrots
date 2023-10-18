import cv2
import numpy as np


def get_segmented_object_position(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_bound = np.array([0, 50, 50])
    upper_bound = np.array([10, 255, 255])

    mask = cv2.inRange(hsv, lower_bound, upper_bound)
    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # Corrected this line

    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(largest_contour)
        return x + w // 2, y + h // 2, w, h  # Return the center position and size of the detected object
    else:
        return None
