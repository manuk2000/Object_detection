import cv2


def read_file(file_path):
    # Read the contents of the file
    with open(file_path, 'r') as file:
        contents = file.read()
        try:
            return eval(contents)  # Evaluate the contents as Python code and return the result
        except:
            print("Ошибка чтения файла")  # Error reading file
            return False


def write_file(file_path, data):
    # Write the data to the file as a string
    with open(file_path, 'w') as file:
        file.write(str(data))


def get_position_to_zoom(video_path, left_zoom, right_zoom, size, times_left_right_zoom):
    video = cv2.VideoCapture(video_path)
    width = size.get("width")
    height = size.get("height")
    time = times_left_right_zoom.get("time")
    time_index = 1
    flag_left_right = True
    scrole = left_zoom
    if times_left_right_zoom.get("start zoom") == "right":
        scrole = right_zoom
        flag_left_right = False
    fps = video.get(cv2.CAP_PROP_FPS)
    count = -1
    output_path = "processed_video.wav"  # Path to save the processed video
    # Codec for writing video in MP4 format
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    output_video = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
    while True:
        count += 1
        ret, frame = video.read()
        if not ret:
            break
        zoomed_frame = cv2.resize(frame, (width, height))
        
        zoomed_frame = zoomed_frame[scrole.get("top"):scrole.get(
            "bottom"), scrole.get("left"): scrole.get("right")]
        output_video.write(zoomed_frame)

        cv2.imshow("Frame", zoomed_frame)
        if cv2.waitKey(1) == 27:
            break
        video_time = count / fps
        if time_index < len(time) and video_time >= time[time_index]:
            time_index += 1
            flag_left_right = not flag_left_right
            if flag_left_right:
                scrole = left_zoom
            else:
                scrole = right_zoom
    video.release()
    output_video.release()
    cv2.destroyAllWindows()


def main(video_path, zoom_position, times_left_right_zoom):
    left_zoom = zoom_position.get("left")
    right_zoom = zoom_position.get("right")
    size = zoom_position.get("size")
    get_position_to_zoom(video_path, left_zoom, right_zoom,
                         size, times_left_right_zoom)


zoom_position_path = "zoom/zoom_position.txt"
zoom_position = read_file(zoom_position_path)

# Read the left/right zoom times data from the file
times_left_right_zoom_path = "zoom/file_times_left_right_zoom.txt"
times_left_right_zoom = read_file(times_left_right_zoom_path)

video_path = "tracking/video1.mp4"
main(video_path, zoom_position, times_left_right_zoom)
