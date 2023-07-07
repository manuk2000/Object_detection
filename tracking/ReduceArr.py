class Reduce:
    def read_file(file_path):
        with open(file_path, 'r') as file:
            contents = file.read()
            try:
                return Reduce.parser(contents)
            except:
                print("Ошибка чтения файла")
                return False
    def parser(contents):
        lines = contents.splitlines()
        result = [(int(line.split(",")[0]), round(float(line.split(",")[1]), 1)) for line in lines]
        return result

    def write_file(file_path, data):
        with open(file_path, 'w') as file:
            file.write(str(data))

    def reduce_of_list(data_list, offset_size):
        new_list = []
        first = data_list[0][0]
        new_list.append((first ,data_list[0][1]) )
        for i in range(len(data_list) - 2):
            if abs(data_list[i + 1][0] - first) > offset_size:
                new_list.append((data_list[i + 1][0] , data_list[i + 1][1]))
                first = data_list[i + 1][0]
        return new_list
    
    def reduce(input_file_path, output_file_path):
        data_list = Reduce.read_file(input_file_path)
        if data_list:
            reduced_data = Reduce.reduce_of_list(data_list, OFSSET_POSSIRION_SIZE)
            Reduce.write_file(output_file_path, reduced_data)
            # print(reduced_data)

OFSSET_POSSIRION_SIZE = 10
input_file_path = "tracking/tracking_position.txt"
output_file_path = "tracking/reduce_tracking_position.txt"
Reduce.reduce(input_file_path, output_file_path)
