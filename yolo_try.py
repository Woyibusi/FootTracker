from ultralytics import YOLO

model = YOLO('yolov8m')

results = model.predict('videos/video1.mp4', save=True)
print(results[0])
print('pro')
print('===================')
for box in results[0].boxes:
    print(box)

