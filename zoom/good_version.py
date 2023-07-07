import cv2

MAX_SCALE_SIZE = 3


def input_number(message):
    user_input = input(message)
    try:
        value = float(user_input)
        return value
    except ValueError:
        return 0


def calculate_new_position(width, height, scale_top_left):
    # Calculate new frame dimensions
    new_height = int(height * scale_top_left.get("scale"))
    new_width = int(width * scale_top_left.get("scale"))

    # # Calculate coordinates for frame cropping
    top = int((new_height - height) / scale_top_left.get("top"))
    bottom = top + height
    left = int((new_width - width) / scale_top_left.get("left"))
    right = left + width

    return {"bottom": bottom, "top": top, "left": left, "right": right, "new_height": new_height, "new_width": new_width}


def input_scale_top_left():
    scale_factor = 0
    while scale_factor < 1 or scale_factor > MAX_SCALE_SIZE:
        message = "Enter the scale factor: "
        scale_factor = input_number(message)

    top = 0
    while top < 1:
        message = "Enter the top offset: "
        top = int(input_number(message))

    left = 0
    while left < 1:
        message = "Enter the left offset: "
        left = int(input_number(message))

    return {"scale": scale_factor, "top": top, "left": left}

def default_scale_top_left():
    return {"scale": 1, "top": 1, "left": 1}


def select_position_zoom_and_scale_factor(video_path):
    # Open the video file
    video = cv2.VideoCapture(video_path)
    print("Please enter the scale factor and offsets:")
    left_right_positions = {}
    key1 = "left"
    key2 = "right"

    scale_top_left = default_scale_top_left()
    flag_start_calculate = True
    flag_barrier_position  = False
    barrier_position = ()
    while True:
        # Read the current frame
        ret, frame = video.read()
        if not ret:
            break

        # Get the frame dimensions
        height, width = frame.shape[:2]

        if flag_start_calculate:
            new_positions = calculate_new_position(
                width, height, scale_top_left)
            flag_start_calculate = False

        # Resize the frame
        zoomed_frame = cv2.resize(frame, (new_positions.get(
            "new_width"), new_positions.get("new_height")))
        zoomed_frame = zoomed_frame[new_positions.get("top"):new_positions.get(
            "bottom"), new_positions.get("left"): new_positions.get("right")]

        if flag_barrier_position:
            num =  int(input("input"))
            text_position =  ((width / 100) * num, int(height / 2)) #coordinates of the text
            cv2.putText(frame, str(
                    "1"), text_position, 0, 1, (0, 0, 255), 2)

        # Display the modified frame
        cv2.imshow('Zoomed Video', zoomed_frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        if len(left_right_positions) == 0 and not flag_barrier_position:
            if '1' == input("Is the left zoom position good? -> 1:"):
                left_right_positions[key1] = {"width" : new_positions.get("new_width") ,"height" : new_positions.get("new_height")}
                
                tmp = new_positions["right"] - new_positions["left"]

                if new_positions["right"] + tmp > new_positions.get("new_width"):
                    tmp = new_positions.get(
                        "new_width") - new_positions["right"]

                new_positions["left"] += tmp
                new_positions["right"] += tmp

                print("Left position is selected")
                print("Please select the right position")
                flag_barrier_position = True
                continue

        else:
            if '1' == input("Is the right zoom position good? -> 1:"):
                left_right_positions[key2] = {"width" : new_positions.get("new_width") ,"height" : new_positions.get("new_height")}
                scale_top_left = default_scale_top_left()
                flag_barrier_position = True
                break
            deviation = 0
            while deviation == 0:
                message = "How much do you want to shift the position to the right: "
                deviation = int(input_number(message))

            deviation = int(
                (new_positions.get("new_width") - width) / deviation)

            if new_positions["right"] + deviation > new_positions.get("new_width"):
                deviation = new_positions.get(
                    "new_width") - new_positions["right"]

            new_positions["left"] += deviation
            new_positions["right"] += deviation
            continue

        if len(left_right_positions) == 0 and not flag_barrier_position:
            scale_top_left = input_scale_top_left()
            new_positions = calculate_new_position(
                width, height, scale_top_left)

    # Close the video file
    video.release()
    cv2.destroyAllWindows()
    return left_right_positions


# Path to the video file
video_path = 'tracking/video1.mp4'

# Apply the zoom effect to the video
scale_top_left = select_position_zoom_and_scale_factor(video_path)
print(scale_top_left)
