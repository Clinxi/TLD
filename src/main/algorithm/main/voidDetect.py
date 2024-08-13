import cv2
from ultralytics import YOLOv10


class VoidDefect:
    def __init__(self, image_path, start_mileage, end_mileage, max_depth):
        self.image_path = image_path
        self.start_mileage = start_mileage
        self.end_mileage = end_mileage
        self.max_depth = max_depth

    def detect(self):
        # Load the YOLOv10 model
        model = YOLOv10(
            'src/main/algorithm/yolov10/weights/void_best_0.587.pt')

        predictions = model.predict(source=self.image_path, show=False, save=False, save_txt=False, classes=[0],
                                    visualize=False)
        img_height, img_width = predictions[0].orig_shape

        results = []
        for box in predictions[0].boxes.xyxy:
            void_start = self.start_mileage + box[0] / img_width * (self.end_mileage - self.start_mileage)
            void_end = self.start_mileage + box[2] / img_width * (self.end_mileage - self.start_mileage)
            void_depth = box[3] / img_height * self.max_depth

            results.append(VoidDefectResult(int(void_start), int(void_end), int(void_depth), 'void'))

        return results


class VoidDefectResult:
    def __init__(self, start_mileage, end_mileage, depth, defect_type):
        self.start_mileage = start_mileage
        self.end_mileage = end_mileage
        self.depth = depth
        self.defect_type = defect_type


if __name__ == '__main__':

    example = VoidDefect(
        "/home/zhangwh/PycharmProject/yolov10/ultralytics/cfg/datasets/image_D2K282+890-700GD/image_D2K282+890-700GD_10.PNG",
        0, 1000, 50)

    results = example.detect()

    print(len(results))
    for result in results:
        print(result.start_mileage, result.end_mileage, result.depth, result.defect_type)
