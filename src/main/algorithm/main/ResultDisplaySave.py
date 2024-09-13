import cv2
import os
import lackingDetect as lD
import voidDetect as vD
import barDetect as bD
from OriginalPhotoInfor import ProcessOriginalPhoto, DetectEventResultWithNewPhoto, DiseaseInformation
from typing import List
import uuid


def merge_near_defect(results, mileage_threshold=0.5):
    """
    合并相近的缺陷
    :param results: 空隙缺陷检测结果列表 list[VoidDefectResult]
    :param mileage_threshold: 判定缺陷是否相近的里程阈值（默认0.5米）
    :return: 合并后的空隙缺陷检测结果列表 list[VoidDefectResult]
    """
    if not results:
        return results
    # 按起始里程排序
    results = sorted(results, key=lambda x: x.start_mileage)
    merged_results = []
    current_result = results[0]
    for i in range(1, len(results)):
        next_result = results[i]
        # 如果下一个缺陷的起始里程与当前缺陷的终止里程很近，则将其合并
        if next_result.start_mileage - current_result.end_mileage <= mileage_threshold:
            # 合并缺陷：取起始最小值，终止最大值，深度范围更新
            current_result.end_mileage = max(current_result.end_mileage, next_result.end_mileage)
            current_result.depth_min = min(current_result.depth_min, next_result.depth_min)
            current_result.depth_max = max(current_result.depth_max, next_result.depth_max)
        else:
            # 当前缺陷已不能合并，保存当前结果并开始新的合并
            merged_results.append(current_result)
            current_result = next_result
    # 保存最后一个合并后的结果
    merged_results.append(current_result)
    return merged_results


class DefectResultDisplay:
    def __init__(self, input_original: ProcessOriginalPhoto):
        self.img = input_original.image
        self.img_real_shape = [input_original.originalMileage, input_original.finialMileage, input_original.depth]
        self.img_pixel_shape = self.img.shape[:2]  # (height, width)
        self.original_photo_name = input_original.originalPhotoName
        self.original_line = input_original.original_line

    def convert_coordinate(self, real_coordinate):
        """
        将实际坐标转换为像素坐标
        :param real_coordinate: 实际坐标 (x_min, x_max, y_min, y_max)
        :return: 像素坐标 (x_min, x_max, y_min, y_max)
        """
        # print(self.img_real_shape, self.img_pixel_shape)
        pixel_x_min = int(self.img_pixel_shape[1] * (real_coordinate[0] - self.img_real_shape[0]) / (
                self.img_real_shape[1] - self.img_real_shape[0])) + 64
        pixel_x_max = int(self.img_pixel_shape[1] * (real_coordinate[1] - self.img_real_shape[0]) / (
                self.img_real_shape[1] - self.img_real_shape[0])) + 64
        pixel_y_min = int(self.img_pixel_shape[0] * real_coordinate[2] / self.img_real_shape[2]) + self.original_line
        pixel_y_max = int(self.img_pixel_shape[0] * real_coordinate[3] / self.img_real_shape[2]) + self.original_line

        # print(
        #     f"Real Coordinate: {real_coordinate} -> Pixel Coordinate: {(pixel_x_min, pixel_x_max, pixel_y_min, pixel_y_max)}")

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
        # print(f"Void Result List: {void_result_list}")
        void_pixel_coordinates = self.get_pixel_coordinates(void_result_list,
                                                            lambda x: x.get_coordinates_list())
        for coord in void_pixel_coordinates:
            # print(f"Drawing rectangle at: {coord}")
            cv2.rectangle(self.img, (coord[0], coord[2]), (coord[1], coord[3]), (0, 255, 0), 4)

    def draw_lack_defects(self, lack_result_list: List[lD.lackingDetectOut]):
        """
        绘制欠厚检测结果
        :param lack_result_list: 欠厚检测结果列表
        """
        lack_pixel_coordinates = self.get_pixel_coordinates(lack_result_list,
                                                            lambda x: [x.diseaseStart, 0, x.actualdepth, 0])
        for coord in lack_pixel_coordinates:
            cv2.arrowedLine(self.img, (coord[0], 40), (coord[0], coord[2]), (0, 0, 255), 4)

    def draw_steel_defects(self, steel_result_list: List[bD.BarDetectResult]):
        """
        绘制钢筋检测结果
        :param steel_result_list: 钢筋检测结果列表
        """
        # print(f"Steel Result List: {steel_result_list}")
        steel_pixel_coordinates = self.get_pixel_coordinates(steel_result_list,
                                                             lambda x: [x.diseaseStart, x.diseaseEnd, 0, 0])
        for coord in steel_pixel_coordinates:
            cv2.line(self.img, (coord[0], self.img_pixel_shape[0] // 2), (coord[1], self.img_pixel_shape[0] // 2),
                     (255, 0, 0), 4)

    def display_and_save_result(self):
        """
        展示检测结果并保存结果图片
        :return: 保存的图片路径, 新图片名称
        """
        # cv2.imshow("result", self.img)
        # cv2.waitKey(0)

        # 获取项目根目录的绝对路径
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__)))))
        result_dir = os.path.join(project_root, 'result')
        # 如果 result 目录不存在，创建该目录
        os.makedirs(result_dir, exist_ok=True)
        # 保存文件
        new_photo_name = str(uuid.uuid4()) + '.png'
        save_path = os.path.join(result_dir, new_photo_name)
        cv2.imwrite(save_path, self.img)

        return save_path, new_photo_name

    def filter_void_defect(self, void_result_list, threshold=100):
        """
        对脱空缺陷进行大津法筛选
        :param void_result_list: 空洞检测结果列表
        :param threshold: 大津法阈值
        :return: 筛选后的空洞检测结果列表
        """
        result_list = []
        void_pixel_coordinates = self.get_pixel_coordinates(void_result_list,
                                                            lambda x: x.get_coordinates_list())
        # 计算全局阈值
        gray_img = cv2.cvtColor(self.img[self.original_line:, 64:], cv2.COLOR_BGR2GRAY)
        gray_img = cv2.blur(gray_img, (25, 25))  # 低通滤波
        global_threshold = cv2.threshold(gray_img, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]
        print(f"Global Threshold: {global_threshold}")
        # 计算全局方差
        global_variance = cv2.Laplacian(gray_img, cv2.CV_64F).var()
        print(f"Global Variance: {global_variance}")
        # 进行大津法筛选
        for i in range(len(void_pixel_coordinates)):
            # 灰度化
            gray_img = cv2.cvtColor(self.img[void_pixel_coordinates[i][2]:void_pixel_coordinates[i][3],
                                    void_pixel_coordinates[i][0]:void_pixel_coordinates[i][1]], cv2.COLOR_BGR2GRAY)
            gray_roi = cv2.blur(gray_img, (25, 25))  # 低通滤波
            # 计算局部阈值
            local_threshold = cv2.threshold(gray_roi, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[0]
            print(f"Local Threshold: {local_threshold}")
            # 计算局部方差
            local_variance = cv2.Laplacian(gray_roi, cv2.CV_64F).var()
            print(f"Local Variance: {local_variance}")
            if local_variance > global_variance:
                result_list.append(void_result_list[i])

        return result_list


# def draw_zigzag_line(self, start_point, end_point, segment_length=20, amplitude=10, color=(255, 0, 0), thickness=2):
#     """
#     绘制折线
#     :param start_point: 起点 (x, y)
#     :param end_point: 终点 (x, y)
#     :param segment_length: 每段折线的长度
#     :param amplitude: 折线的高度差
#     :param color: 线的颜色
#     :param thickness: 线的粗细
#     """
#     points = []
#     x_direction = 1 if end_point[0] > start_point[0] else -1
#     y_direction = 1 if end_point[1] > start_point[1] else -1
#     x, y = start_point
#
#     while (x < end_point[0] and x_direction == 1) or (x > end_point[0] and x_direction == -1):
#         points.append((x, y))
#         x += segment_length * x_direction
#         y += amplitude * y_direction
#         y_direction *= -1
#
#     points.append(end_point)
#
#     for i in range(len(points) - 1):
#         cv2.line(self.img, points[i], points[i + 1], color, thickness)


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
    void_result_list = merge_near_defect(void_result_list)  # 合并相近的脱空缺陷
    void_result_list = example.filter_void_defect(void_result_list, threshold=140)  # 进行大津法筛选
    example.draw_void_defects(void_result_list)
    # print(void_result_list)

    new_photo_address, new_photo_name = example.display_and_save_result()

    disease_information_list = []
    for void_result in void_result_list:
        if void_result is not None:
            result = DiseaseInformation(void_result.start_mileage, void_result.end_mileage,
                                        void_result.depth_min, void_result.defect_type)
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
