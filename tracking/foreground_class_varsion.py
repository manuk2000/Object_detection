import cv2
import numpy as np
from object_detection import ObjectDetection
import math


class Tracking:
    # If no tracking_object is present, set position; otherwise, throw "Not found object" error
    @staticmethod
    def not_have_tracking_object(center_points_cur_frame, center_points_prev_frame, tracking_object):
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.dist((pt[0], pt[1]), (pt2[0], pt2[1]))
                if distance < 20:
                    tracking_object.append(pt)  # Set Object position
                    return
        if not len(tracking_object) == 0:
            print("Not found object")

    # If tracking_object is present, update position; otherwise, clear tracking_object
    @staticmethod
    def have_tracking_object(center_points_cur_frame, tracking_object):
        for pt in center_points_cur_frame:
            distance = math.hypot(
                tracking_object[0][0] - pt[0], tracking_object[0][1] - pt[1])
            if distance < 20:
                tracking_object[0] = pt  # Update Object position
                return
        # If no object is present, clear tracking_object
        tracking_object.clear()

    # Detect objects on frame
    @staticmethod
    def detect_objects_on_frame(center_points_cur_frame, od, frame):
        (class_ids, scores, boxes) = od.detect(frame)
        for box in boxes:
            (x, y, w, h) = box
            cx = int((x + x + w)/2)
            cy = int(y)
            center_points_cur_frame.append((cx, cy))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    @staticmethod
    def tracking(file_name):
        # Initialize Object Detection
        if file_name is None:
            print("File not found")
        od = ObjectDetection()

        cap = cv2.VideoCapture(file_name)

        return_tracking_position = []

        # Initialize count
        center_points_prev_frame = []

        tracking_object = []  # List to store tracking object position

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # Point current frame
            center_points_cur_frame = []
            Tracking.detect_objects_on_frame(
                center_points_cur_frame, od, frame)

            if len(tracking_object) == 0:
                Tracking.not_have_tracking_object(
                    center_points_cur_frame, center_points_prev_frame, tracking_object)
            elif len(tracking_object) != 0:
                Tracking.have_tracking_object(
                    center_points_cur_frame, tracking_object)

            if len(tracking_object) == 1:
                cv2.circle(frame, tracking_object[0], 5, (0, 200, 0), -1)
                cv2.putText(frame, str(
                    "1"), (tracking_object[0][0], tracking_object[0][1] - 7), 0, 1, (0, 0, 255), 2)

            cv2.imshow("Frame", frame)

            if cv2.waitKey(3) == 27:
                break
            center_points_prev_frame = center_points_cur_frame

            if len(tracking_object) == 1:
                return_tracking_position.append(tracking_object[0])

        cap.release()
        cv2.destroyAllWindows()
        return return_tracking_position

res = Tracking.tracking("tracking/video1.mp4")
print(res)
