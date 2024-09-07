import cv2
import numpy as np


class lackingDetectIn:
    def __init__(self, image_path, startingMileage, endingMileage, standardThickness, vertical_resolution,
                 horizontal_resolution):
        self.imageAdress = image_path
        self.startingMileage = startingMileage
        self.endingMileage = endingMileage
        self.standardThickness = standardThickness
        self.vertical_resolution = vertical_resolution
        self.horizontal_resolution = horizontal_resolution

    def detect(self, window_width, window_height, step_size, thresh):
        # y_min=280
        y_min=(self.standardThickness-0.08)/self.vertical_resolution
        image = cv2.imread(self.imageAdress)
        h, w = image.shape[0], image.shape[1]
        black_regions = []
        for x in range(0, w - window_width + 1, step_size):
            for y in range(0, h - window_height + 1, step_size):
                window = image[y:y + window_height, x:x + window_width]
                if np.mean(window) < thresh:
                    if not black_regions:
                        if y > y_min:
                            black_regions.append((x, y))
                            break
                    else:
                        if y > y_min:
                            black_regions.append((x, y))
                            break
        design_hight = self.standardThickness / self.vertical_resolution
        print("vertical is ",self.vertical_resolution)
        # print("lackDetet height is ",design_hight)
        result = [lackingDetectOut(self.transxposition(x), y*self.vertical_resolution) for (x, y) in black_regions if y < design_hight]
        finial_result=self.optimize_result_list(result)
        return finial_result

    def transxposition(self, x):
        if self.startingMileage<self.endingMileage:
            real_x = self.startingMileage + x * self.horizontal_resolution
        else:
            real_x = self.startingMileage - x * self.horizontal_resolution
        revise_x = round(real_x, 3)
        return revise_x
    def optimize_result_list(self,result):
        """
        :param result:原始数据对象列表
        :return min_values: 邻近区域中深度最小对象列表
        """
        threshold = 0.2  # 定义一个阈值来识别相近区段
        min_values = []

        current_segment = []
        current_min = float('inf')
        current_min_x = None

        for i, coord in enumerate(result):
            if i == 0 or abs(coord.diseaseStart - result[i - 1].diseaseStart) < threshold:
                current_segment.append(coord)
                if coord.actualdepth < current_min:
                    current_min = coord.actualdepth
                    current_min_x = coord.diseaseStart
            else:
                # 新的区段开始，保存上一区段的最小值和对应的X
                min_values.append(lackingDetectOut(current_min_x, current_min))
                # 重置当前区段
                current_segment = [coord]
                current_min = coord.actualdepth
                current_min_x = coord.diseaseStart

        # 保存最后一个区段的最小值和对应的X
        if current_segment:
            min_values.append(lackingDetectOut(current_min_x, current_min))
        return min_values


class lackingDetectOut:
    def __init__(self, diseaseStart, actualdepth):
        self.diseaseStart = diseaseStart
        # self.diseaseEnd=diseaseEnd
        self.actualdepth = actualdepth
