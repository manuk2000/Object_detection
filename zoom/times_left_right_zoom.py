# Define the class Reduce
class Reduce:
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

    def zoom_determining_time_moving(x_time, barrier_position):
        # Determine the zoom time based on the x_time and barrier position
        left = barrier_position.get("left")
        right = barrier_position.get("right")
        start_zoom = "right"
        left_flag = True
        right_flag = False
        res_time = [x_time[0][1]]
        if x_time[0][0] < left:
            start_zoom = "left"
            left_flag = False
            right_flag = True
        for frame in x_time:
            if frame[0] < left and left_flag:
                res_time.append(frame[1])
                left_flag = False
                right_flag = True
            elif frame[0] > right and right_flag:
                res_time.append(frame[1])
                right_flag = False
                left_flag = True
        return {"time": res_time, "start zoom": start_zoom}

    def get_barrier_position(file_path):
        # Read the barrier position from the file
        zoom_positions = Reduce.read_file(file_path)
        barrier_position = zoom_positions.get("barrier")
        return {"left": barrier_position.get("left")[0], "right": barrier_position.get("right")[0]}


barrier_position_file_path = "zoom/zoom_position.txt"
barrier_position = Reduce.get_barrier_position(barrier_position_file_path)

x_time_file_path = "tracking/reduce_tracking_position.txt"
x_time = Reduce.read_file(x_time_file_path)

res = Reduce.zoom_determining_time_moving(x_time, barrier_position)
out_file = "zoom/file_times_left_right_zoom.txt"
Reduce.write_file(out_file, res)
