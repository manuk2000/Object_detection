import cv2

MAX_SCALE_SIZE = 3  # Maximum scale size allowed

def write_file(file_path, data):
    with open(file_path, 'w') as file:
        file.write(str(data))

def input_number(message):
    user_input = input(message)
    try:
        value = float(user_input)  # Parse user input as a float
        return value
    except ValueError:
        return 0  # Return 0 if input cannot be parsed as a float

# Function to calculate the new position based on scale factor and offsets
def calculate_new_position(width, height, scale_top_left):
    new_height = int(height * scale_top_left.get("scale"))
    new_width = int(width * scale_top_left.get("scale"))

    bottom = new_height - int((height * scale_top_left.get("top")) / 100)
    top = bottom - height

    left = int((width * scale_top_left.get("left")) / 100)
    right = left + width

    return {"bottom": bottom, "top": top, "left": left, "right": right, "new_height": new_height, "new_width": new_width}

def input_scale_top_left():
    scale_factor = 0
    while scale_factor < 1 or scale_factor > MAX_SCALE_SIZE:
        message = "Enter the scale factor: "
        scale_factor = input_number(message)

    top = -1
    while top < 0 or top >= 50:
        message = "Enter the bottom offset in percentages: "
        top = int(input_number(message))

    left = -1
    while left < 0 or left >= 50:
        message = "Enter the left offset in percentages: "
        left = int(input_number(message))

    return {"scale": scale_factor, "top": top, "left": left}

def default_scale_top_left():
    return {"scale": 1, "top": 0, "left": 0}

def set_barrier_dot():
    message_left = "Input the left dot in percentages: "
    left_dot = int(input_number(message_left))
    message_right = "Input the right dot in percentages: "
    right_dot = int(input_number(message_right))
    return {"left": left_dot, "right": right_dot}

def calculate_percent(number, percent):
    return int((number / 100) * percent)

def select_position_zoom_and_scale_factor(video_path, output_file_path):
    video = cv2.VideoCapture(video_path)
    print("Please enter the scale factor and offsets:")
    left_right_positions = {}
    key1 = "left"
    key2 = "right"
    key3 = "size"
    key4 = "barrier"

    scale_top_left = default_scale_top_left()
    flag_start_calculate = True
    flag_start_barrier_calculate = False
    flag_barrier_position = False
    barrier_position = {"left": 0, "right": 0}

    while True:
        ret, frame = video.read()
        if not ret:
            break

        height, width = frame.shape[:2]

        if flag_start_calculate or flag_barrier_position:
            new_positions = calculate_new_position(width, height, scale_top_left)
            flag_start_calculate = False

        zoomed_frame = cv2.resize(frame, (new_positions.get("new_width"), new_positions.get("new_height")))
        zoomed_frame = zoomed_frame[new_positions.get("top"):new_positions.get("bottom"), new_positions.get("left"): new_positions.get("right")]

        if flag_barrier_position and flag_start_barrier_calculate:
            center_height = int(height / 2)
            barrier_position = set_barrier_dot()
            left_dot = (calculate_percent(width, barrier_position.get("left")), center_height)
            right_dot = (width - calculate_percent(width, barrier_position.get("right")), center_height)
            
            barrier_position = {"left": left_dot, "right": right_dot}

            if frame.shape[0] > 0 and frame.shape[1] > 0:
                cv2.putText(zoomed_frame, str("1"), left_dot, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                cv2.putText(zoomed_frame, str("1"), right_dot, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

        cv2.imshow('Zoomed Video', zoomed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if len(left_right_positions) == 0 and not flag_barrier_position:
            if '1' == input("Is the left zoom position good? -> 1:"):
                left_right_positions[key1] = dict(zip(new_positions , list(new_positions.values())[:-2]))

                tmp = new_positions["right"] - new_positions["left"]

                if new_positions["right"] + tmp > new_positions.get("new_width"):
                    tmp = new_positions.get("new_width") - new_positions["right"]

                new_positions["left"] += tmp
                new_positions["right"] += tmp

                print("Left position is selected")
                print("Please select the right position")
                continue

        elif not flag_barrier_position:
            if '1' == input("Is the right zoom position good? -> 1:"):
                left_right_positions[key2] = dict(zip(new_positions , list(new_positions.values())[:-2]))
                left_right_positions[key3] = {"width": new_positions.get("new_width"), "height": new_positions.get("new_height")}
                scale_top_left = default_scale_top_left()
                flag_barrier_position = True
                print("Please input percentages of barrier dot positions")
                continue

            deviation = 0
            while deviation == 0:
                message = "How much do you want to shift the position to the right: "
                deviation = int(input_number(message))

            deviation = int((width * deviation) / 100)
            
            if new_positions["left"] - deviation < 0:
                deviation = new_positions["left"]

            new_positions["left"] += deviation
            new_positions["right"] += deviation
            continue

        if len(left_right_positions) == 0:
            scale_top_left = input_scale_top_left()
            new_positions = calculate_new_position(width, height, scale_top_left)

        if flag_barrier_position and flag_start_barrier_calculate:
            if '1' == input("Is the barrier dots position good? -> 1:"):
                left_right_positions[key4] = barrier_position
                break

        if flag_barrier_position:
            flag_start_barrier_calculate = True

    video.release()
    cv2.destroyAllWindows()
    write_file(output_file_path, left_right_positions)
    return left_right_positions

# Path to the video file
video_path = 'tracking/video1.mp4'
file_path_zoom_position = "zoom/zoom_position.txt"

# Apply the zoom effect to the video and store the zoom positions and scale factors
scale_top_left = select_position_zoom_and_scale_factor(video_path, file_path_zoom_position)
print(scale_top_left)
