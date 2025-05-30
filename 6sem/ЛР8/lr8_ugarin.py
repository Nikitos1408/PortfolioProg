import cv2

def highlightFace(net, frame, conf_threshold=0.7):
    frameOpencvDnn = frame.copy()
    frameHeight = frameOpencvDnn.shape[0]
    frameWidth = frameOpencvDnn.shape[1]
    blob = cv2.dnn.blobFromImage(frameOpencvDnn, 1.0, (300, 300), [104, 117, 123], True, False)
    net.setInput(blob)
    detections = net.forward()
    faceBoxes = []
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > conf_threshold:
            x1 = int(detections[0, 0, i, 3] * frameWidth)
            y1 = int(detections[0, 0, i, 4] * frameHeight)
            x2 = int(detections[0, 0, i, 5] * frameWidth)
            y2 = int(detections[0, 0, i, 6] * frameHeight)
            faceBoxes.append([x1, y1, x2, y2])
            cv2.rectangle(frameOpencvDnn, (x1, y1), (x2, y2), (0, 255, 0), int(round(frameHeight / 150)), 8)
    return frameOpencvDnn, faceBoxes

faceProto = "opencv_face_detector.pbtxt"
faceModel = "opencv_face_detector_uint8.pb"
faceNet = cv2.dnn.readNet(faceModel, faceProto)
print("Модель загружена")

def process_image_file(image_path):
    image = cv2.imread(image_path)
    if image is None:
        print(f"Не удалось открыть изображение: {image_path}")
        return
    resultImg, faceBoxes = highlightFace(faceNet, image, conf_threshold=0.5)
    if not faceBoxes:
        print("Лица не распознаны")
    else:
        print(f"Найдено лиц: {len(faceBoxes)}")
    cv2.imshow("Face detection", resultImg)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def process_camera():
    video = cv2.VideoCapture(0)
    while cv2.waitKey(1) < 0:
        hasFrame, frame = video.read()
        if not hasFrame:
            cv2.waitKey()
            break
        resultImg, faceBoxes = highlightFace(faceNet, frame, conf_threshold=0.5)
        if not faceBoxes:
            print("Лица не распознаны")
        cv2.imshow("Face detection", resultImg)
    video.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    print("Выберите режим работы:")
    print("1 — обработать изображение из файла")
    print("2 — работать с камерой")
    mode = input("Введите 1 или 2 и нажмите Enter: ").strip()
    if mode == "1":
        filename = input("Введите имя файла (например, test1.png): ").strip()
        process_image_file(filename)
    elif mode == "2":
        process_camera()
    else:
        print("Некорректный выбор. Перезапустите программу.")