import os
import cv2

import img_processing as ip
import lackingDetect as lD
import voidDetect as vD
from barDetect import BarInfor


class DiseaseInformation:
    def __init__(self, diseaseStart, diseaseEnd, diseaseDepth, diseaseType):
        self.diseaseStart = diseaseStart
        self.diseaseEnd = diseaseEnd
        self.diseaseDepth = diseaseDepth
        # void, lackDepth, lackBar 
        self.diseaseType = diseaseType

    def __str__(self):
        return f"DiseaseInformation(diseaseStart={self.diseaseStart},diseaseEnd={self.diseaseEnd}, diseaseDepth={self.diseaseDepth}, diseaseType='{self.diseaseType}')"

    def to_dict(self):
        return {
            "diseaseStart": self.diseaseStart,
            "diseaseEnd": self.diseaseEnd,
            "diseaseDepth": self.diseaseDepth,
            "diseaseType": self.diseaseType
        }


class DetectOriginalPhoto:
    def __init__(self, originalPhotoAddress, originalPhotoName):
        self.originalPhotoAddress = originalPhotoAddress
        self.originalPhotoName = originalPhotoName

    def __repr__(self):
        return f"DetectOriginalPhoto(originalPhotoAddress='{self.originalPhotoAddress}', originalPhotoName='{self.originalPhotoName}')"


class ProjectStandard:
    def __init__(self, startingMileage, endingMileage, standardSteelBarSpacing, standardThickness):
        self.startingMileage = startingMileage
        self.endingMileage = endingMileage
        self.standardSteelBarSpacing = standardSteelBarSpacing
        self.standardThickness = standardThickness

    def __repr__(self):
        return (f"ProjectStandard(startingMileage={self.startingMileage}, "
                f"endingMileage={self.endingMileage}, "
                f"standardSteelBarSpacing={'素混凝土' if self.standardSteelBarSpacing == 0 else self.standardSteelBarSpacing}, "
                f"standardThickness={self.standardThickness})")


class DetectEventResultWithNewPhoto:
    def __init__(self, newPhotoAddress=None, newPhotoName=None, diseaseInformationList=None):
        self.newPhotoAddress = newPhotoAddress
        self.newPhotoName = newPhotoName
        self.diseaseInformationList = diseaseInformationList if diseaseInformationList is not None else []

    def getNewPhotoAddress(self):
        return self.newPhotoAddress

    def setNewPhotoAddress(self, newPhotoAddress):
        self.newPhotoAddress = newPhotoAddress

    def getNewPhotoName(self):
        return self.newPhotoName

    def setNewPhotoName(self, newPhotoName):
        self.newPhotoName = newPhotoName

    def getDiseaseInformationList(self):
        return self.diseaseInformationList

    def setDiseaseInformationList(self, diseaseInformationList):
        self.diseaseInformationList = diseaseInformationList

    def __str__(self):
        return (f"DetectEventResultWithNewPhoto(newPhotoAddress='{self.newPhotoAddress}', "
                f"newPhotoName='{self.newPhotoName}', "
                f"diseaseInformationList={self.diseaseInformationList})")

    def to_dict(self):
        return {
            "newPhotoAddress": self.newPhotoAddress,
            "newPhotoName": self.newPhotoName,
            "diseaseInformationList": [diseaseInfo.to_dict() for diseaseInfo in self.diseaseInformationList]
        }


class APhotoWithStandards:
    def __init__(self, detectOriginalPhoto, projectStandards):
        self.detectOriginalPhoto = DetectOriginalPhoto(**detectOriginalPhoto)
        self.projectStandards = [ProjectStandard(**ps) for ps in projectStandards]

    def __repr__(self):
        return f"APhotoWithStandards(detectOriginalPhoto={self.detectOriginalPhoto}, projectStandards={self.projectStandards})"


class ProcessOriginalPhoto:
    """
    读取输入图片，获取图片基本信息
    """

    def __init__(self, photo: DetectOriginalPhoto):
        self.originalPhotoAddress = photo.originalPhotoAddress
        self.originalPhotoName = photo.originalPhotoName
        self.image = cv2.imread(photo.originalPhotoAddress)
        self.originalMileage = None
        self.finialMileage = None
        self.depth = None
        self.original_line = None
        self.horizontal_resolution = None
        self.vertical_resolution = None

    def get_basic_information(self):
        self.get_original_line()
        self.get_originalMileage()
        self.get_finialMileage()
        self.get_horizontal_resolution()
        self.get_depth()
        self.get_vertical_resolution()
        print("get information success")

    def get_original_line(self):
        original_line = ip.horizon_line(self.image[:, 63:64])
        if original_line:
            self.original_line = original_line.pop() + 1
        else:
            raise ValueError("No horizontal line found in the specified range.")

    def get_originalMileage(self):
        try:
            head_number = self.image[8:20, 62:112]  # 感兴趣的数字区域 横向 第一个数值
            rheadnum = ip.split_num(head_number)
        except ValueError:
            try:
                head_number = self.image[8:20, 121:176]
                rheadnum = ip.split_num(head_number) - 1
            except ValueError:
                head_number = self.image[10:26, 130:196]
                rheadnum = ip.split_num(head_number) - 1
        self.originalMileage = rheadnum

    def get_finialMileage(self):
        try:
            tail_number = self.image[8:20, -191:-92]
            rtailnum = ip.split_num(tail_number)
            rtailnum = ip.tailnum_revise(rtailnum)
        except ValueError:
            try:
                tail_number = self.image[8:20, -140:-92]  # 数段读取区域设置
                rtailnum = ip.split_num(tail_number)
                rtailnum = ip.tailnum_revise(rtailnum)
            except ValueError:
                tail_number = self.image[10:25, -132:-85]
                rtailnum = ip.split_num(tail_number)
                rtailnum = ip.tailnum_revise(rtailnum)
        self.finialMileage = rtailnum

    def get_horizontal_resolution(self):
        horizontal_res = abs(self.originalMileage - self.finialMileage) / (self.image.shape[1] - 1 - 64)
        self.horizontal_resolution = horizontal_res

    def get_depth(self):
        num_position = self.image[self.original_line:, 13:48]
        self.depth = ip.get_tailnum(num_position)

    def get_vertical_resolution(self):
        vertical_position = self.image[self.original_line:, 48:54]  # (水平，垂直)
        black_lines = ip.find_black_horizontal_lines(vertical_position)
        vertical_resolution = ip.compute_vertical_resolution(self.depth, black_lines)
        self.vertical_resolution = vertical_resolution

    def create_steel_example(self, projectStandards):
        steel_example_list = []
        for standard in projectStandards:
            if standard.standardSteelBarSpacing != 0:
                data = self.image[self.original_line:, 65:-2]
                split_start = int(abs(self.originalMileage - standard.startingMileage) / self.horizontal_resolution)
                split_end = int(abs(self.originalMileage - standard.endingMileage) / self.horizontal_resolution)
                # print(split_start, split_end)
                splitpict = data[:, split_start:split_end]  # 选取所有行，截取列
                # self.image = splitpict
                directory_path = os.path.dirname(self.originalPhotoAddress)
                folder_path = os.path.join(directory_path, "steelbardetect")
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                # self.address = file_path
                window_pixel = int(7 / self.horizontal_resolution)
                step_pixel = int(5 / self.horizontal_resolution)
                n = 0
                for i in range(0, splitpict.shape[1], step_pixel):
                    if i + window_pixel > splitpict.shape[1]:
                        # 如果剩余部分不足，则从右向左切取最后的window_pixel宽度
                        i = splitpict.shape[1] - window_pixel
                    sample = splitpict[:, i:i + window_pixel]
                    file_name = f"{standard.startingMileage + n * 5}——{standard.startingMileage + n * 5 + 7}.png"
                    file_path = os.path.join(folder_path, file_name)
                    if not cv2.imwrite(file_path, sample):
                        print("fail save ", file_path)
                    barinfor_example = BarInfor(file_path, standard.startingMileage + n * 5,
                                                standard.startingMileage + n * 5 + 7,
                                                standard.standardSteelBarSpacing)
                    steel_example_list.append(barinfor_example)
                    n += 1
        return steel_example_list

    def creat_void_example(self):
        result = []
        data = self.image[self.original_line:, 65:-1]
        directory_path = os.path.dirname(self.originalPhotoAddress)
        folder_path = os.path.join(directory_path, "voiddetect")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        n = 0
        img_width = ip.find_verticalline(data)
        if self.originalMileage < self.finialMileage:
            for i in range(0, data.shape[1], img_width):
                image = data[:, i: i + img_width - 1]
                # filename=f"{self.originalPhotoName+n*5}.png"
                file_name = f"{self.originalMileage + n * 5}——{self.originalMileage + n * 5 + 5}.png"
                file_path = os.path.join(folder_path, file_name)
                if not cv2.imwrite(file_path, image):
                    print("fail save:", file_path)
                example = vD.VoidDefect(file_path, self.originalMileage + n * 5, self.originalMileage + n * 5 + 5,
                                        self.depth)
                n += 1
                result.append(example)
        else:
            for i in range(0, data.shape[1], img_width):
                image = data[:, i: i + img_width - 1]

                file_name = f"{self.originalMileage - n * 5}—{self.originalMileage - n * 5 - 5}.png"
                file_path = os.path.join(folder_path, file_name)
                # file_path = os.path.join(folder_path, str(self.originalMileage - n * 5), "__",
                #                          str(self.originalMileage - n * 5-5), ".png")
                if not cv2.imwrite(file_path, image):
                    print("fail save:", file_path)
                example = vD.VoidDefect(file_path, self.originalMileage - n * 5, self.originalMileage - n * 5 - 5,
                                        self.depth)
                n += 1
                result.append(example)
        return result

    def create_lacking_example(self, projectStandards):
        lacking_example_list = []
        for standard in projectStandards:
            data = self.image[self.original_line:, 65:-2]
            split_start = int(abs(self.originalMileage - standard.startingMileage) / self.horizontal_resolution)
            split_end = int(abs(self.originalMileage - standard.endingMileage) / self.horizontal_resolution)
            splitpict = data[:, split_start:split_end]  # 选取所有行，截取列
            directory_path = os.path.dirname(self.originalPhotoAddress)
            folder_path = os.path.join(directory_path, "lackingdetect")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_name = f"{standard.startingMileage}——{standard.endingMileage}.png"
            file_path = os.path.join(folder_path, file_name)
            # file_path = os.path.join(folder_path, str(standard.startingMileage), "——", str(standard.endingMileage), ".png")
            if not cv2.imwrite(file_path, splitpict):
                print("fail save", file_path)
            lining_example = lD.lackingDetectIn(file_path, standard.startingMileage, standard.endingMileage,
                                                standard.standardThickness, self.vertical_resolution,
                                                self.horizontal_resolution)
            lacking_example_list.append(lining_example)
        return lacking_example_list
