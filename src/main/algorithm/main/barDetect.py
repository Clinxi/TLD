import cv2
import torch
import numpy as np
from ultralytics.data.augment import LetterBox
from ultralytics.nn.autobackend import AutoBackend
import matplotlib.pyplot as plt

def preprocess_letterbox(image):
    letterbox = LetterBox(new_shape=640, stride=32, auto=True)
    image = letterbox(image=image)
    image = (image[..., ::-1] / 255.0).astype(np.float32) # BGR to RGB, 0 - 255 to 0.0 - 1.0
    image = image.transpose(2, 0, 1)[None]  # BHWC to BCHW (n, 3, h, w)
    image = torch.from_numpy(image)
    return image

def preprocess_warpAffine(image, dst_width=640, dst_height=640):
    scale = min((dst_width / image.shape[1], dst_height / image.shape[0]))
    ox = (dst_width  - scale * image.shape[1]) / 2
    oy = (dst_height - scale * image.shape[0]) / 2
    M = np.array([
        [scale, 0, ox],
        [0, scale, oy]
    ], dtype=np.float32)
    
    img_pre = cv2.warpAffine(image, M, (dst_width, dst_height), flags=cv2.INTER_LINEAR,
                             borderMode=cv2.BORDER_CONSTANT, borderValue=(114, 114, 114))
    IM = cv2.invertAffineTransform(M)

    img_pre = (img_pre[...,::-1] / 255.0).astype(np.float32)
    img_pre = img_pre.transpose(2, 0, 1)[None]
    img_pre = torch.from_numpy(img_pre)
    return img_pre, IM

def postprocess(pred, IM=[], conf_thres=0.25):

    # 输入是模型推理的结果，即8400个预测框
    # 1,8400,84 [cx,cy,w,h,class*80]
    boxes = []
    for item in pred[0]:
        cx, cy, w, h = item[:4]
        label = item[4:].argmax()
        confidence = item[4 + label]
        if confidence < conf_thres:
            continue
        left    = cx - w * 0.5
        top     = cy - h * 0.5
        right   = cx + w * 0.5
        bottom  = cy + h * 0.5
        boxes.append([left, top, right, bottom, confidence, label])

    boxes = np.array(boxes)
    lr = boxes[:,[0, 2]]
    tb = boxes[:,[1, 3]]
    boxes[:,[0,2]] = IM[0][0] * lr + IM[0][2]
    boxes[:,[1,3]] = IM[1][1] * tb + IM[1][2]
    
    return boxes

def hsv2bgr(h, s, v):
    h_i = int(h * 6)
    f = h * 6 - h_i
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    
    r, g, b = 0, 0, 0

    if h_i == 0:
        r, g, b = v, t, p
    elif h_i == 1:
        r, g, b = q, v, p
    elif h_i == 2:
        r, g, b = p, v, t
    elif h_i == 3:
        r, g, b = p, q, v
    elif h_i == 4:
        r, g, b = t, p, v
    elif h_i == 5:
        r, g, b = v, p, q

    return int(b * 255), int(g * 255), int(r * 255)

def random_color(id):
    h_plane = (((id << 2) ^ 0x937151) % 100) / 100.0
    s_plane = (((id << 3) ^ 0x315793) % 100) / 100.0
    return hsv2bgr(h_plane, s_plane, 1)


def cal_bar(model_path_list, img_pre, IM):
    max_count=0
    for model_path in model_path_list:
        model  = AutoBackend(weights=model_path)
        result = model(img_pre)['one2one'][0].transpose(-1, -2) # 1,8400,84
        boxes  = postprocess(result, IM)
        count = 0
        for obj in boxes:
            count += 1
        max_count = max(max_count, count)
    return max_count
    

# 缺筋检测算法输入
class BarInfor():
    def __init__(self, address, startingMileage, endingMileage, standardSteelBarSpacing):
        self.imageAddress = address             # 传给缺筋检测算法的图片位置
        self.startingMileage = startingMileage  # 检测图片的开始位置  
        self.endingMileage = endingMileage      # 检测图片的结束位置
        self.standardSteelBarSpacing = standardSteelBarSpacing  # 标准钢筋间距
    def detect(self):
        pass
        model_path_list = ["src/main/algorithm/yolov10/weights/bar_run4_last.pt",
                           "src/main/algorithm/yolov10/weights/bar_run5_last.pt",
                           "src/main/algorithm/yolov10/weights/bar_run11_last.pt",
                           "src/main/algorithm/yolov10/weights/bar_run17_last.pt"]
        diseaStart = self.startingMileage
        diseaEnd = self.endingMileage
        img = cv2.imread(self.imageAddress)
        img_pre, IM = preprocess_warpAffine(img)
        
        count = cal_bar(model_path_list=model_path_list, img_pre=img_pre, IM=IM)
        
        actualSpace = count / (self.endingMileage - self.startingMileage)
        isDisease = False
        if actualSpace / self.standardSteelBarSpacing < 0.8:
            isDisease = True
        result = BarDetectResult(diseaseStart=diseaStart, diseaseEnd=diseaEnd, actualSpace=actualSpace, isDiease=isDisease)
        return result
    
# 缺筋检测算法输出
class BarDetectResult:
    def __init__(self, diseaseStart, diseaseEnd, actualSpace, isDiease=False):
        self.diseaseStart = diseaseStart    # 缺陷开始的位置
        self.diseaseEnd = diseaseEnd        # 缺陷结束的位置
        self.actualSpace = actualSpace      # 实际的钢筋间距
        self.isDiease = isDiease            # 是否为缺陷
    def __str__(self):
        # 返回一个描述对象的字符串
        isDiease_str = 'Yes' if self.isDiease else 'No'
        return (f"BarDetectResult(Disease Start: {self.diseaseStart}, "
                f"Disease End: {self.diseaseEnd}, "
                f"Actual Space: {self.actualSpace}, "
                f"Is Disease: {isDiease_str})")
    
    
       

if __name__ == "__main__": 
    img_address = "/home/disk3/jsa/projects/yolov10/data_build/data/all_rebar/1_2.PNG"
    test = BarInfor(img_address, 1, 2, 8)
    result = test.detect()
    print(result)