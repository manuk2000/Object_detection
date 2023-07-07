import cv2

def zoom_video(input_path, output_path, scale_factor):
    # Открываем видеофайл
    video = cv2.VideoCapture(input_path)

    # Получаем свойства исходного видео
    width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = video.get(cv2.CAP_PROP_FPS)
    print(width)
    print(height)
    # Создаем объект VideoWriter для сохранения увеличенного видео
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, fps, (int(width * scale_factor), int(height * scale_factor)))

    while video.isOpened():
        ret, frame = video.read()

        if not ret:
            break

        # Масштабируем кадр с использованием коэффициента масштабирования
        zoomed_frame = cv2.resize(frame, (int(width * scale_factor), int(height * scale_factor)))

        # Проверяем размеры увеличенного кадра
        zoomed_width = zoomed_frame.shape[1]
        zoomed_height = zoomed_frame.shape[0]

        # # Выводим размеры увеличенного кадра для проверки
        # print("Ширина увеличенного кадра:", zoomed_width)
        # print("Высота увеличенного кадра:", zoomed_height)

        # Записываем увеличенный кадр в выходной видеофайл
        out.write(zoomed_frame)

        cv2.imshow('Увеличенное видео', zoomed_frame)
        # return
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Освобождаем ресурсы
    video.release()
    out.release()
    cv2.destroyAllWindows()

# Пример использования
input_video_path = 'resize_to_2HD/input_video.mp4'
output_video_path = 'resize_to_2HD/output_video.mp4'
zoom_scale = 1.5 # Увеличение на 50%

zoom_video(input_video_path, output_video_path, zoom_scale)
