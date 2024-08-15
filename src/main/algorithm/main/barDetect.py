import cv2
import torch
import numpy as np
from ultralytics.nn.autobackend import AutoBackend
import matplotlib.pyplot as plt


def postprocess(pred, conf_thres=0.25):
    # 输入是模型推理的结果，即8400个预测框
    # 1,8400,84 [cx,cy,w,h,class*80]
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


def cal_bar(model_path_list, img_pre):
    max_count = 0
    for model_path in model_path_list:
        model = AutoBackend(weights=model_path)
        result = model(img_pre)['one2one'][0].transpose(-1, -2)  # 1,8400,84
        # print(result.shape)
        boxes = postprocess(result)
        count = 0
        for obj in boxes:
            count += 1
        max_count = max(max_count, count)
    return max_count


def image_to_tensor_cv(image_path, target_size=(224, 224)):
    # 1. 读取图像
    image = cv2.imread(image_path)  # OpenCV 默认以 BGR 读取图像
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)  # 转换为 RGB
    # 3. 归一化像素值
    image = image / 255.0

    # 4. 转换颜色通道顺序
    image = image.transpose(2, 0, 1)  # 从 (高, 宽, 通道) 转换为 (通道, 高, 宽)

    # 5. 添加批次维度
    image = image[None, :]  # 从 (通道, 高, 宽) 转换为 (批次, 通道, 高, 宽)

    # 6. 转换为 PyTorch 张量
    image_tensor = torch.from_numpy(image).float()

    return image_tensor


# 缺筋检测算法输入
class BarInfor():
    def __init__(self, address, startingMileage, endingMileage, standardSteelBarSpacing):
        self.imageAddress = address  # 传给缺筋检测算法的图片位置
        self.startingMileage = startingMileage  # 检测图片的开始位置  
        self.endingMileage = endingMileage  # 检测图片的结束位置
        self.standardSteelBarSpacing = standardSteelBarSpacing  # 标准钢筋间距

    def detect(self):
        pass
        # model_path_list = [r"D:\PycharmProjects\TLD\src\main\algorithm\main\weights\bar_run4_last.pt",
        #                    r"D:\PycharmProjects\TLD\src\main\algorithm\main\weights\bar_run5_last.pt",
        #                    r"D:\PycharmProjects\TLD\src\main\algorithm\main\weights\bar_run11_last.pt",
        #                    r"D:\PycharmProjects\TLD\src\main\algorithm\main\weights\bar_run17_last.pt"]
        model_path_list = ["src/main/algorithm/main/weights/bar_run4_last.pt",
                           "src/main/algorithm/main/weights/bar_run5_last.pt",
                           "src/main/algorithm/main/weights/bar_run11_last.pt",
                           "src/main/algorithm/main/weights/bar_run17_last.pt"
                           ]

        diseaStart = self.startingMileage
        diseaEnd = self.endingMileage
        img = cv2.imread(self.imageAddress)
        img_pre = image_to_tensor_cv(self.imageAddress)
        count = cal_bar(model_path_list=model_path_list, img_pre=img_pre)

        actualSpace = (self.endingMileage - self.startingMileage) / count
        
        isDisease = False
        print(f"count: {count}")
        print(f"actualSpace: {actualSpace}")
        if actualSpace / self.standardSteelBarSpacing > 1.05:
            isDisease = True
        result = BarDetectResult(diseaseStart=diseaStart, diseaseEnd=diseaEnd, actualSpace=actualSpace,
                                 isDiease=isDisease)
        if result.isDiease:
            return result
        return None


# 缺筋检测算法输出
class BarDetectResult:
    def __init__(self, diseaseStart, diseaseEnd, actualSpace, isDiease=False):
        self.diseaseStart = diseaseStart  # 缺陷开始的位置
        self.diseaseEnd = diseaseEnd  # 缺陷结束的位置
        self.actualSpace = actualSpace  # 实际的钢筋间距
        self.isDiease = isDiease  # 是否为缺陷

    def __str__(self):
        # 返回一个描述对象的字符串
        isDiease_str = 'Yes' if self.isDiease else 'No'
        return (f"BarDetectResult(Disease Start: {self.diseaseStart}, "
                f"Disease End: {self.diseaseEnd}, "
                f"Actual Space: {self.actualSpace}, "
                f"Is Disease: {isDiease_str})")


if __name__ == "__main__":
    # img_address = r"D:\PycharmProjects\TLD\src\main\algorithm\test\case1\steelbardetect\324450——324504.png"
    img_address = "/home/disk3/jsa/projects/TLD/src/main/algorithm/test/case1/steelbardetect/324450——324504.png"
    test = BarInfor(img_address, 1, 2, 8)
    result = test.detect()
    print(result)
