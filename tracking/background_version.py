import cv2
import numpy as np
from object_detection import ObjectDetection
import math


class Tracking:
    MIN_MOVEMENT_OBJECT = 30

    @staticmethod
    def write_file(file_path, data):
        # Write tracking position data to a file
        with open(file_path, 'w') as file:
            for position in data:
                file.write(f"{position.cx},{position.time}\n")

    @staticmethod
    def not_have_tracking_object(center_points_cur_frame, center_points_prev_frame, tracking_object):
        # Find a new tracking object if not already tracking
        for pt in center_points_cur_frame:
            for pt2 in center_points_prev_frame:
                distance = math.dist((pt[0], pt[1]), (pt2[0], pt2[1]))
                if distance < Tracking.MIN_MOVEMENT_OBJECT:
                    tracking_object.append(pt)
                    return
        if not len(tracking_object) == 0:
            print("Not found object")

    @staticmethod
    def have_tracking_object(center_points_cur_frame, tracking_object):
        # Update the position of the tracking object
        for pt in center_points_cur_frame:
            distance = math.hypot(
                tracking_object[0][0] - pt[0], tracking_object[0][1] - pt[1])
            if distance < Tracking.MIN_MOVEMENT_OBJECT:
                tracking_object[0] = pt
                return
        tracking_object.clear()

    @staticmethod
    def detect_objects_on_frame(center_points_cur_frame, od, frame, video_time):
        # Detect objects on the frame and record their positions
        (class_ids, scores, boxes) = od.detect(frame)
        for box in boxes:
            (x, y, w, h) = box
            cx = int((x + x + w) / 2)
            cy = int(y)
            center_points_cur_frame.append((cx, cy, video_time))
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    @staticmethod
    def tracking(file_name, file_path):
        if file_name is None:
            print("File not found")
        od = ObjectDetection()
        cap = cv2.VideoCapture(file_name)
        fps = cap.get(cv2.CAP_PROP_FPS)
        return_tracking_position = []
        center_points_prev_frame = []
        tracking_object = []
        count = 0
        max_frames = 10
        while count < max_frames:
            print(count)
            ret, frame = cap.read()
            if not ret:
                break
            center_points_cur_frame = []
            video_time = count / fps
            Tracking.detect_objects_on_frame(
                center_points_cur_frame, od, frame, video_time)
            if len(tracking_object) == 0:
                Tracking.not_have_tracking_object(
                    center_points_cur_frame, center_points_prev_frame, tracking_object)
            elif len(tracking_object) != 0:
                Tracking.have_tracking_object(
                    center_points_cur_frame, tracking_object)
            center_points_prev_frame = center_points_cur_frame
            if len(tracking_object) == 1:
                position = TrackingPosition(tracking_object[0][0], video_time)
                return_tracking_position.append(position)
            count += 1
        cap.release()
        cv2.destroyAllWindows()
        Tracking.write_file(file_path, return_tracking_position)
        return return_tracking_position


class TrackingPosition:
    def __init__(self, cx, time):
        self.cx = cx
        self.time = time


vidieo_path = "tracking/video1.mp4"
file_path = "tracking/tracking_position.txt"
res = Tracking.tracking(vidieo_path, file_path)
