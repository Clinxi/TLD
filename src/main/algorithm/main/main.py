import json
import os
import sys

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
        # self.get_vertical_resolution()
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
        black_lines = ip.split_num(vertical_position)
        vertical_resolution = ip.compute_vertical_resolutio(self.depth, black_lines)
        self.vertical_resolution = vertical_resolution

    def create_steel_example(self, projectStandards):
        steel_example_list = []
        for standard in projectStandards:
            if standard.standardSteelBarSpacing:
                data = self.image[self.original_line:, 65:-2]
                split_start = int(abs(self.originalMileage - standard.startMileage) / self.horizontal_resolution)
                split_end = int(abs(self.originalMileage - standard.endingMileage) / self.horizontal_resolution)
                splitpict = data[:, split_start:split_end]  # 选取所有行，截取列
                # self.image = splitpict
                directory_path = os.path.dirname(self.originalPhotoAddress)
                folder_path = os.path.join(directory_path, "steelbardetect")
                if not os.path.exists(folder_path):
                    os.makedirs(folder_path)
                file_path = os.path.join(folder_path, str(self.startMileage), "——", str(self.endingMileage), ".png")
                cv2.imwrite(file_path, splitpict)
                # self.address = file_path
                barinfor_example = BarInfor(file_path, standard.startMileage, standard.endingMileage,
                                            standard.standardSteelBarSpacing)
                steel_example_list.append(barinfor_example)
                return steel_example_list

    def creat_void_example(self):
        result = []
        data = self.image[self.original_line:, 65:-2]
        directory_path = os.path.dirname(self.originalPhotoAddress)
        folder_path = os.path.join(directory_path, "voiddetect")
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        n = 0
        img_width = ip.find_verticalline(data)
        if self.original_line < self.finialMileage:
            for i in range(0, data.shape[1], img_width):
                image = data[:, i: i + img_width]
                # filename=f"{self.originalPhotoName+n*5}.png"
                file_path = os.path.join(folder_path, str(self.startMileage + n * 5), "——",
                                         str(self.startMileage + n * 5) + 5, ".png")
                cv2.imwrite(file_path, self.image)
                example = vD.VoidDefect(file_path, self.startMileage + n * 5, self.startMileage + n * 5 + 5, self.depth)
                n += 1
                result.append(example)
        else:
            for i in range(0, data.shape[1], img_width):
                image = data[:, i: i + img_width]
                # filename=f"{self.originalPhotoName+n*5}.png"
                file_path = os.path.join(folder_path, str(self.startMileage - n * 5), "——",
                                         str(self.startMileage - n * 5) - 5, ".png")
                cv2.imwrite(file_path, self.image)
                example = vD.VoidDefect(file_path, self.startMileage - n * 5, self.startMileage - n * 5 - 5, self.depth)
                n += 1
                result.append(example)
        return result

    def create_lacking_example(self, projectStandards):
        lacking_example_list = []
        for standard in projectStandards:
            data = self.image[self.original_line:, 65:-2]
            split_start = int(abs(self.originalMileage - standard.startMileage) / self.horizontal_resolution)
            split_end = int(abs(self.originalMileage - standard.endingMileage) / self.horizontal_resolution)
            splitpict = data[:, split_start:split_end]  # 选取所有行，截取列
            directory_path = os.path.dirname(self.originalPhotoAddress)
            folder_path = os.path.join(directory_path, "lackingdetect")
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)
            file_path = os.path.join(folder_path, str(self.startMileage), "——", str(self.endingMileage), ".png")
            cv2.imwrite(file_path, splitpict)
            lining_example = lD.lackingDetectIn(file_path, standard.startMileage, standard.endingMileage,
                                                standard.standardThinckness, self.vertical_resolution,
                                                self.horizontal_resolution)
            lacking_example_list.append(lining_example)
        return lacking_example_list
    # this is there the algorithm exists


def perform_detection(photo_with_standards_list):
    # example
    results = []
    disease_info_1 = DiseaseInformation(1.0, 10.5, 2.0, "Leaf Spot")
    disease_info_2 = DiseaseInformation(1.0, 15.0, 3.5, "Powdery Mildew")
    disease_information_list = [disease_info_1, disease_info_2]

    # ----------------------------------------#

    for photo_with_standards in photo_with_standards_list:
        photo = photo_with_standards.detectOriginalPhoto
        projectstandards = photo_with_standards.projectStandards
        input_original = ProcessOriginalPhoto(photo)
        # 大图获取信息
        input_original.get_basic_information()
        #创建三个缺陷对象列表
        lack_object_list = input_original.create_lacking_example(projectstandards)
        steel_object_list = input_original.create_steel_example(projectstandards)
        void_object_list = input_original.creat_void_example()
        # 这里可以根据需要使用 projectStandards 列表进行额外的计算或检测
        result = DetectEventResultWithNewPhoto(
            newPhotoAddress=photo.originalPhotoAddress,
            newPhotoName=photo.originalPhotoName,
            diseaseInformationList=disease_information_list
        )
        results.append(result)
    return results


def main(photos_with_standards_json):
    photo_with_standards_data = json.loads(photos_with_standards_json)
    photo_with_standards_list = [APhotoWithStandards(**pws) for pws in photo_with_standards_data]

    results = perform_detection(photo_with_standards_list)
    return [result.to_dict() for result in results]


if __name__ == "__main__":
    # 从标准输入读取 JSON 字符串

    input_json = sys.stdin.read()

    # # 调用 main 函数处理输入数据并输出结果
    output = main(input_json)
    print(json.dumps(output))
