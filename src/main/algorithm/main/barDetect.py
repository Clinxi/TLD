import cv2
import numpy as np
import torch
from src.main.algorithm.yolov10.ultralytics.nn.autobackend import AutoBackend


def postprocess(pred, conf_thres=0.25):
    boxes = []
    for item in pred[0]:
        cx, cy, w, h = item[:4]
        label = item[4:].argmax()
        confidence = item[4 + label]
        if confidence < conf_thres:
            continue
        left = cx - w * 0.5
        top = cy - h * 0.5
        right = cx + w * 0.5
        bottom = cy + h * 0.5
        boxes.append([left, top, right, bottom, confidence, label])

    boxes = np.array(boxes)
    return boxes


def cal_bar(model_list, img_pre):
    max_count = 0
    for model in model_list:
        result = model(img_pre)['one2one'][0].transpose(-1, -2)
        boxes = postprocess(result)
        count = 0
        for obj in boxes:
            count += 1
        max_count = max(max_count, count)
    return max_count


def image_to_tensor_cv(image_path, target_size=(224, 224)):
    image = cv2.imread(image_path)
    h = (image.shape[0] // 32) * 32 + 32
    w = 2*(image.shape[1] // 32) * 32 + 32
    image = cv2.resize(image, (w, h), interpolation=cv2.INTER_LINEAR)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image / 255.0
    image = image.transpose(2, 0, 1)
    image = image[None, :]
    image_tensor = torch.from_numpy(image).float()
    return image_tensor


class BarInfor():
    def __init__(self, address, startingMileage, endingMileage, standardSteelBarSpacing,
                 model_path_list=None):
        if model_path_list is None:
            model_path_list = ["src/main/algorithm/main/weights/bar_run4_last.pt",
                               "src/main/algorithm/main/weights/bar_run5_last.pt",
                               "src/main/algorithm/main/weights/bar_run11_last.pt",
                               "src/main/algorithm/main/weights/bar_run17_last.pt"
                               ]
        self.imageAddress = address
        self.startingMileage = startingMileage
        self.endingMileage = endingMileage
        self.standardSteelBarSpacing = standardSteelBarSpacing
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.model = [AutoBackend(weights=model_path).to(self.device) for model_path in model_path_list]

    def detect(self):
        diseaStart = self.startingMileage
        diseaEnd = self.endingMileage
        img_pre = image_to_tensor_cv(self.imageAddress).to(self.device)
        count = cal_bar(model_list=self.model, img_pre=img_pre) + 2
        if count != 0:
            actualSpace = (self.endingMileage - self.startingMileage) / count
        else:
            actualSpace = 0
        isDisease = False
        if actualSpace / self.standardSteelBarSpacing > 1.1:
            isDisease = True
        result = BarDetectResult(diseaseStart=diseaStart, diseaseEnd=diseaEnd, actualSpace=actualSpace,
                                 isDiease=isDisease)
        if result.isDiease:
            return result
        return None


class BarDetectResult:
    def __init__(self, diseaseStart, diseaseEnd, actualSpace, isDiease=False):
        self.diseaseStart = diseaseStart
        self.diseaseEnd = diseaseEnd
        self.actualSpace = actualSpace
        self.isDiease = isDiease

    def __str__(self):
        isDiease_str = 'Yes' if self.isDiease else 'No'
        return (f"BarDetectResult(Disease Start: {self.diseaseStart}, "
                f"Disease End: {self.diseaseEnd}, "
                f"Actual Space: {self.actualSpace}, "
                f"Is Disease: {isDiease_str})")


if __name__ == "__main__":
    img_address = "/home/disk3/jsa/projects/TLD/src/main/algorithm/test/case1/steelbardetect/324450——324504.png"
    test = BarInfor(img_address, 1, 2, 8)
    result = test.detect()
    print(result)
