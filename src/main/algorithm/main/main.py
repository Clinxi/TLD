import json
import os
import io
import sys

import cv2

import img_processing as ip
import lackingDetect as lD
import voidDetect as vD
import barDetect as bD
from ResultDisplaySave import get_new_photo_address
from OriginalPhotoInfor import DiseaseInformation, DetectEventResultWithNewPhoto, ProcessOriginalPhoto, APhotoWithStandards

def disable_print():
    sys.stdout = io.StringIO()


def enable_print():
    sys.stdout = sys.__stdout__




def perform_detection(photo_with_standards_list) -> list[DetectEventResultWithNewPhoto]:
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
        # 创建三个缺陷对象列表
        lack_object_list = input_original.create_lacking_example(projectstandards)
        steel_object_list = input_original.create_steel_example(projectstandards)
        void_object_list = input_original.creat_void_example()

        # 创建三种缺陷结果列表
        lack_result_list = [result for lack_object in lack_object_list for result in
                            lack_object.detect()]  # list[lackingDetectOut]
        steel_result_list = [steel_object.detect() for steel_object in steel_object_list]  # list[BarDetectResult]
        void_result_list = [result for void_object in void_object_list for result in
                            void_object.detect()]  # list[VoidDefectResult]

        result = get_new_photo_address(input_original, lack_result_list, steel_result_list,
                                       void_result_list)

        # # 这里可以根据需要使用 projectStandards 列表进行额外的计算或检测
        # result = DetectEventResultWithNewPhoto(
        #     newPhotoAddress=photo.originalPhotoAddress,
        #     newPhotoName=photo.originalPhotoName,
        #     diseaseInformationList=disease_information_list
        # )
        results.append(result)
    return results


def main(photos_with_standards_json):
    photo_with_standards_data = json.loads(photos_with_standards_json)
    photo_with_standards_list = [APhotoWithStandards(**pws) for pws in photo_with_standards_data]

    results = perform_detection(photo_with_standards_list)
    return [result.to_dict() for result in results]


def test(photos_with_standards_json):
    # photo_with_standards_data = json.loads(photos_with_standards_json)
    photo_with_standards_list = [APhotoWithStandards(**pws) for pws in photos_with_standards_json]
    for photo_with_standards in photo_with_standards_list:
        photo = photo_with_standards.detectOriginalPhoto
        projectstandards = photo_with_standards.projectStandards
        input_original = ProcessOriginalPhoto(photo)
        # 大图获取信息
        input_original.get_basic_information()
        # 创建三个缺陷对象列表
        lack_object_list = input_original.create_lacking_example(projectstandards)
        steel_object_list = input_original.create_steel_example(projectstandards)
        void_object_list = input_original.creat_void_example()
        print("void length:", len(void_object_list))
        print("lack length :", len(lack_object_list))
        print("steel length :", len(steel_object_list))
    return "ok"


if __name__ == "__main__":
    # # 从标准输入读取 JSON 字符串

    # input_json = sys.stdin.read()

    # # # 调用 main 函数处理输入数据并输出结果
    # output = main(input_json)
    # print(json.dumps(output))

    # -------------------------below is test code----------------------------- 
    disable_print()
    json_file_path = r"src/main/algorithm/test/case1/case1.json"
    with open(json_file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    print(type(data))
    output = test(data)
    enable_print()
    print(output)
