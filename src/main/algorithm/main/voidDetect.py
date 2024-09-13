import cv2
from ultralytics import YOLOv10


class VoidDefect:
    def __init__(self, image_path, start_mileage, end_mileage, max_depth,
                 net=YOLOv10('src/main/algorithm/main/weights/best_x3.pt')):
        """
        初始化空隙缺陷检测类
        :param image_path: 图片路径
        :param start_mileage: 起始里程
        :param end_mileage: 终止里程
        :param max_depth: 最大深度
        :param net: 网络模型
        """
        self.image_path = image_path
        self.start_mileage = start_mileage
        self.end_mileage = end_mileage
        self.max_depth = max_depth
        self.model = net

    def detect(self):
        """
        空隙缺陷检测
        :return: 空隙缺陷检测结果列表 list[VoidDefectResult]
        """
        # 使用 YOLOv10 模型进行预测
        predictions = self.model.predict(source=self.image_path, show=False, save=False, save_txt=False, classes=[1],
                                         visualize=False, device=["cpu"])
        img_height, img_width = predictions[0].orig_shape

        # # 打印检测类别，确保只处理类别 0 的情况
        # print("----------")
        # print(predictions[0].boxes.cls)
        # print("----------")

        results = []

        # 遍历预测结果中的框，只处理类别 0 的框
        for i, box in enumerate(predictions[0].boxes.xyxy):
            # 只处理标签为 0 的框
            if predictions[0].boxes.cls[i] == 1:
                # 计算实际的里程
                void_start = self.start_mileage + box[0] / img_width * (self.end_mileage - self.start_mileage)
                void_end = self.start_mileage + box[2] / img_width * (self.end_mileage - self.start_mileage)
                void_depth_min = box[1] / img_height * self.max_depth
                void_depth_max = box[3] / img_height * self.max_depth

                # 过滤掉深度不符合要求的框
                if 0.2 < void_depth_max < 1 and void_depth_max - void_depth_min > 0.1:
                    results.append(
                        VoidDefectResult(void_start, void_end, void_depth_min, void_depth_max, 'void'))

        return results


class VoidDefectResult:
    def __init__(self, start_mileage, end_mileage, depth_min, depth_max, defect_type):
        """
        初始化空隙缺陷检测结果类
        :param start_mileage: 起始里程
        :param end_mileage: 终止里程
        :param depth_min: 最小深度
        :param depth_max: 最大深度
        :param defect_type: 缺陷类型
        """
        self.start_mileage = start_mileage.item()
        self.end_mileage = end_mileage.item()
        self.depth_min = depth_min.item()
        self.depth_max = depth_max.item()
        self.defect_type = defect_type

    def __repr__(self):
        return (f"start_mileage: {self.start_mileage}, end_mileage: {self.end_mileage},depth_min: {self.depth_min}, "
                f"depth_max: {self.depth_max}, defect_type: {self.defect_type}")

    def get_coordinates_list(self):
        """
        获取缺陷的坐标列表
        :return: 缺陷的坐标列表 [start_mileage, end_mileage, depth_min, depth_max]
        """
        return [self.start_mileage, self.end_mileage, self.depth_min, self.depth_max]


if __name__ == '__main__':

    example = VoidDefect(
        "/home/zhangwh/PycharmProject/yolov10/ultralytics/cfg/datasets/image_D2K282+890-700GD/image_D2K282+890-700GD_14.PNG",
        0, 1000, 50)

    results = example.detect()

    print(len(results))
    for result in results:
        print(result.get_coordinates_list())

# import cv2
# import torch
# import numpy as np
# from ultralytics.data.augment import LetterBox
# from ultralytics.nn.autobackend import AutoBackend
# import matplotlib.pyplot as plt
#
#
# def preprocess_letterbox(image):
#     letterbox = LetterBox(new_shape=640, stride=32, auto=True)
#     image = letterbox(image=image)
#     image = (image[..., ::-1] / 255.0).astype(np.float32)  # BGR to RGB, 0 - 255 to 0.0 - 1.0
#     image = image.transpose(2, 0, 1)[None]  # BHWC to BCHW (n, 3, h, w)
#     image = torch.from_numpy(image)
#     return image
#
#
# def preprocess_warpAffine(image, dst_width=640, dst_height=640):
#     scale = min((dst_width / image.shape[1], dst_height / image.shape[0]))
#     ox = (dst_width - scale * image.shape[1]) / 2
#     oy = (dst_height - scale * image.shape[0]) / 2
#     M = np.array([
#         [scale, 0, ox],
#         [0, scale, oy]
#     ], dtype=np.float32)
#
#     img_pre = cv2.warpAffine(image, M, (dst_width, dst_height), flags=cv2.INTER_LINEAR,
#                              borderMode=cv2.BORDER_CONSTANT, borderValue=(114, 114, 114))
#     IM = cv2.invertAffineTransform(M)
#
#     img_pre = (img_pre[..., ::-1] / 255.0).astype(np.float32)
#     img_pre = img_pre.transpose(2, 0, 1)[None]
#     img_pre = torch.from_numpy(img_pre)
#     return img_pre, IM
#
#
# def iou(box1, box2):
#     def area_box(box):
#         return (box[2] - box[0]) * (box[3] - box[1])
#
#     left = max(box1[0], box2[0])
#     top = max(box1[1], box2[1])
#     right = min(box1[2], box2[2])
#     bottom = min(box1[3], box2[3])
#     cross = max((right - left), 0) * max((bottom - top), 0)
#     union = area_box(box1) + area_box(box2) - cross
#     if cross == 0 or union == 0:
#         return 0
#     return cross / union
#
#
# def NMS(boxes, iou_thres):
#     remove_flags = [False] * len(boxes)
#
#     keep_boxes = []
#     for i, ibox in enumerate(boxes):
#         if remove_flags[i]:
#             continue
#
#         keep_boxes.append(ibox)
#         for j in range(i + 1, len(boxes)):
#             if remove_flags[j]:
#                 continue
#
#             jbox = boxes[j]
#             if (ibox[5] != jbox[5]):
#                 continue
#             if iou(ibox, jbox) > iou_thres:
#                 remove_flags[j] = True
#     return keep_boxes
#
#
# def postprocess(pred, IM=[], conf_thres=0.25, iou_thres=0.45):
#     # 输入是模型推理的结果，即8400个预测框
#     # 1,8400,84 [cx,cy,w,h,class*80]
#     boxes = []
#     for item in pred[0]:
#         cx, cy, w, h = item[:4]
#         label = item[4:].argmax()
#         confidence = item[4 + label]
#         if confidence < conf_thres:
#             continue
#         left = cx - w * 0.5
#         top = cy - h * 0.5
#         right = cx + w * 0.5
#         bottom = cy + h * 0.5
#         boxes.append([left, top, right, bottom, confidence, label])
#
#     boxes = np.array(boxes)
#     lr = boxes[:, [0, 2]]
#     tb = boxes[:, [1, 3]]
#     boxes[:, [0, 2]] = IM[0][0] * lr + IM[0][2]
#     boxes[:, [1, 3]] = IM[1][1] * tb + IM[1][2]
#     boxes = sorted(boxes.tolist(), key=lambda x: x[4], reverse=True)
#
#     return NMS(boxes, iou_thres)
#
#
# def hsv2bgr(h, s, v):
#     h_i = int(h * 6)
#     f = h * 6 - h_i
#     p = v * (1 - s)
#     q = v * (1 - f * s)
#     t = v * (1 - (1 - f) * s)
#
#     r, g, b = 0, 0, 0
#
#     if h_i == 0:
#         r, g, b = v, t, p
#     elif h_i == 1:
#         r, g, b = q, v, p
#     elif h_i == 2:
#         r, g, b = p, v, t
#     elif h_i == 3:
#         r, g, b = p, q, v
#     elif h_i == 4:
#         r, g, b = t, p, v
#     elif h_i == 5:
#         r, g, b = v, p, q
#
#     return int(b * 255), int(g * 255), int(r * 255)
#
#
# def random_color(id):
#     h_plane = (((id << 2) ^ 0x937151) % 100) / 100.0
#     s_plane = (((id << 3) ^ 0x315793) % 100) / 100.0
#     return hsv2bgr(h_plane, s_plane, 1)
#
#
# def cal_bar(model_path_list, img_pre, IM):
#     max_count = 0
#     for model_path in model_path_list:
#         model = AutoBackend(weights=model_path)
#         result = model(img_pre)['one2one'][0].transpose(-1, -2)  # 1,8400,84
#         boxes = postprocess(result, IM)
#         count = 0
#         for obj in boxes:
#             count += 1
#         max_count = max(max_count, count)
#     return max_count
#
#
# class VoidDefect:
#     def __init__(self, image_path, start_mileage, end_mileage, max_depth):
#         self.image_path = image_path
#         self.start_mileage = start_mileage
#         self.end_mileage = end_mileage
#         self.max_depth = max_depth
#
#     def detect(self):
#         # Load the YOLOv10 model
#         img = cv2.imread(self.image_path)
#         img_height, img_width = img.shape[:2]
#         img_pre, IM = preprocess_warpAffine(img)
#         model = AutoBackend(
#             weights='/home/zhangwh/PycharmProject/yolov10/runs/detect/freeze9_data_198_K_yolov10b_0.01_0.013/weights/best_0.587.pt')
#         result = model(img_pre)['one2one'][0].transpose(-1, -2)  # 1,8400,84
#
#         boxes = postprocess(result, IM)
#
#         results = []
#         for obj in boxes:
#             left, top, right, bottom = int(obj[0]), int(obj[1]), int(obj[2]), int(obj[3])
#             results.append([left, top, right, bottom])
#
#         for i, box in enumerate(results):
#             # 计算实际的里程
#             void_start = self.start_mileage + box[0] / img_width * (self.end_mileage - self.start_mileage)
#             void_end = self.start_mileage + box[2] / img_width * (self.end_mileage - self.start_mileage)
#             void_depth_min = box[3] / img_height * self.max_depth
#             void_depth_max = box[1] / img_height * self.max_depth
#
#             results[i] = VoidDefectResult(int(void_start), int(void_end), int(void_depth_min), int(void_depth_max),
#                                           'void')
#
#         return results
#
#
# class VoidDefectResult:
#     def __init__(self, start_mileage, end_mileage, depth_min, depth_max, defect_type):
#         self.start_mileage = start_mileage
#         self.end_mileage = end_mileage
#         self.depth_min = depth_min
#         self.depth_max = depth_max
#         self.defect_type = defect_type
#
#
# if __name__ == '__main__':
#     example = VoidDefect(
#         "/home/zhangwh/PycharmProject/yolov10/ultralytics/cfg/datasets/image_D2K282+890-700GD/image_D2K282+890-700GD_10.PNG",
#         0, 1000, 50)
#
#     results = example.detect()
#
#     print(len(results))
#     for result in results:
#         print(result.start_mileage, result.end_mileage, result.depth_min, result.depth_max, result.defect_type)
