import cv2
import os
import lackingDetect as lD
import voidDetect as vD
import barDetect as bD
from OriginalPhotoInfor import ProcessOriginalPhoto, DetectEventResultWithNewPhoto, DiseaseInformation
from typing import List


class DefectResultDisplay:
    def __init__(self, input_original: ProcessOriginalPhoto):
        self.img = input_original.image
        self.img_real_shape = [input_original.originalMileage, input_original.finialMileage, input_original.depth]
        self.img_pixel_shape = self.img.shape[:2]
        self.original_photo_name = input_original.originalPhotoName

    def convert_coordinate(self, real_coordinate):
        """
        将实际坐标转换为像素坐标
        :param real_coordinate: 实际坐标 (x_min, x_max, y_min, y_max)
        :return: 像素坐标 (x_min, x_max, y_min, y_max)
        """
        pixel_x_min = int(self.img_pixel_shape[0] * (real_coordinate[0] - self.img_real_shape[0]) / (
                self.img_real_shape[1] - self.img_real_shape[0]))
        pixel_x_max = int(self.img_pixel_shape[0] * (real_coordinate[1] - self.img_real_shape[0]) / (
                self.img_real_shape[1] - self.img_real_shape[0]))
        pixel_y_min = int(self.img_pixel_shape[1] * real_coordinate[2] / self.img_real_shape[2])
        pixel_y_max = int(self.img_pixel_shape[1] * real_coordinate[3] / self.img_real_shape[2])

        return pixel_x_min, pixel_x_max, pixel_y_min, pixel_y_max

    def get_pixel_coordinates(self, result_list, coordinate_func):
        """
        获取检测结果的像素坐标
        :param result_list: 检测结果列表
        :param coordinate_func: 获取坐标的函数
        :return: 像素坐标列表
        """
        return [self.convert_coordinate(coordinate_func(result)) for result in result_list if result is not None]

    def draw_void_defects(self, void_result_list: List[vD.VoidDefectResult]):
        """
        绘制空洞检测结果
        :param void_result_list: 空洞检测结果列表
        """
        void_pixel_coordinates = self.get_pixel_coordinates(void_result_list,
                                                            lambda x: x.get_coordinates_list())
        for coord in void_pixel_coordinates:
            cv2.rectangle(self.img, (coord[0], coord[2]), (coord[1], coord[3]), (0, 255, 0), 2)

    def draw_lack_defects(self, lack_result_list: List[lD.lackingDetectOut]):
        """
        绘制欠厚检测结果
        :param lack_result_list: 欠厚检测结果列表
        """
        lack_pixel_coordinates = self.get_pixel_coordinates(lack_result_list,
                                                            lambda x: [x.diseaseStart, 0, x.actualdepth, 0])
        for coord in lack_pixel_coordinates:
            cv2.arrowedLine(self.img, (coord[0], 5), (coord[0], coord[2]), (0, 0, 255), 2)

    def draw_steel_defects(self, steel_result_list: List[bD.BarDetectResult]):
        """
        绘制钢筋检测结果
        :param steel_result_list: 钢筋检测结果列表
        """
        steel_pixel_coordinates = self.get_pixel_coordinates(steel_result_list,
                                                             lambda x: [x.diseaseStart, x.diseaseEnd, 0, 0])
        for coord in steel_pixel_coordinates:
            cv2.line(self.img, (coord[0], self.img_pixel_shape[1] // 2), (coord[1], self.img_pixel_shape[1] // 2),
                     (255, 0, 0), 2)

    def display_and_save_result(self):
        """
        展示检测结果并保存结果图片
        :return: 保存的图片路径
        """
        # cv2.imshow("result", self.img)
        # cv2.waitKey(0)

        # 获取项目根目录的绝对路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        result_dir = os.path.join(project_root, 'result')
        # 如果 result 目录不存在，创建该目录
        os.makedirs(result_dir, exist_ok=True)
        # 保存文件
        save_path = os.path.join(result_dir, self.original_photo_name)
        cv2.imwrite(save_path, self.img)
        print(f"Result saved to {save_path}")

        return save_path


def get_and_save_new_photo(input_original: ProcessOriginalPhoto,
                           void_result_list: List[vD.VoidDefectResult],
                           lack_result_list: List[lD.lackingDetectOut],
                           steel_result_list: List[bD.BarDetectResult]):
    """
    返回 DetectEventResultWithNewPhoto 类型
    :param input_original: 输入的原始图片为 ProcessOriginalPhoto 类型
    :param void_result_list: 空洞检测结果列表
    :param lack_result_list: 欠厚检测结果列表
    :param steel_result_list: 钢筋检测结果列表
    :return:
    """
    example = DefectResultDisplay(input_original)
    example.draw_lack_defects(lack_result_list)
    example.draw_steel_defects(steel_result_list)
    example.draw_void_defects(void_result_list)

    new_photo_address = example.display_and_save_result()

    disease_information_list = []
    for void_result in void_result_list:
        if void_result is not None:
            result = DiseaseInformation(void_result.start_mileage, void_result.end_mileage, void_result.depth_min,
                                        void_result.defect_type)
            disease_information_list.append(result)

    for steel_result in steel_result_list:
        if steel_result is not None:
            result = DiseaseInformation(steel_result.diseaseStart, steel_result.diseaseEnd, steel_result.actualSpace,
                                        "lack steel")
            disease_information_list.append(result)

    for lack_result in lack_result_list:
        if lack_result is not None:
            result = DiseaseInformation(lack_result.diseaseStart, lack_result.diseaseStart, lack_result.actualdepth,
                                        "lack depth")
            disease_information_list.append(result)

    return DetectEventResultWithNewPhoto(new_photo_address, example.original_photo_name,
                                         disease_information_list)


if __name__ == '__main__':
    pass
