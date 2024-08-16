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
        image = cv2.imread(self.imageAdress)
        h, w = image.shape[0], image.shape[1]
        black_regions = []
        # print("h,w",h,w)
        for x in range(0, w - window_width + 1, step_size):
            for y in range(0, h - window_height + 1, step_size):
                window = image[y:y + window_height, x:x + window_width]

                if np.mean(window) < thresh:
                    if not black_regions:
                        if y > 280:
                            black_regions.append((x, y))
                            break
                    else:
                        if y > 280:
                            black_regions.append((x, y))
                            break
        design_hight = self.standardThickness / self.vertical_resolution
        result = [lackingDetectOut(self.transxposition(x), y/1000) for (x, y) in black_regions if y < design_hight]
        return result

    def transxposition(self, x):
        real_x = self.startingMileage + x * self.horizontal_resolution
        revise_x = round(real_x, 3)
        return revise_x


class lackingDetectOut:
    def __init__(self, diseaseStart, actualdepth):
        self.diseaseStart = diseaseStart
        # self.diseaseEnd=diseaseEnd
        self.actualdepth = actualdepth
