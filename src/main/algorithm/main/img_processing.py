import os

import cv2 as cv
import numpy as np

import number_processing


def cv_show(name, img):
    """定义cv_show函数，用于显示图像"""
    cv.namedWindow(name, cv.WINDOW_NORMAL)  # 窗口大小可调
    cv.resizeWindow(name, img.shape[1], img.shape[0])  # 窗口大小可调
    cv.imshow(name, img)
    cv.waitKey(0)
    cv.destroyAllWindows()


def cv_info(name, img):
    """
    定义cv_info函数，确认图像是否成功读取，并且打印图像的基本信息
    """
    print(f"图像 {name} 信息如下：")
    if img is None:
        print("无法读取图像")
    else:
        print("图像数据类型：", img.dtype)
        print("图像类型：", type(img))
        print("图像尺寸：", img.shape)
        print("图像行数：", img.shape[0])
        print("图像列数：", img.shape[1])
    print()


def find_verticalline(img):
    """
    定义find_verticalline函数，用于寻找垂直分界线
    返回一段图像的宽度
    """
    for i in range(img.shape[1]):  # 遍历 a 列
        if np.all(img[0, i] >= [230, 230, 230]):
            # 求该列像素均值，判断是否为白色
            mean = np.mean(img[:, i])
            if mean >= 240:  # 像素均值大于 230 判断为白色
                # print(f"分界线位置：{i}, 像素均值：{mean}", end="\n\n")
                return i+1
    return -1  # 如果没有找到符合条件的分界线，则返回图像的宽度


def horizon_line(img):
    """
        寻找图片中的所有黑色水平线
        返回所有黑线的行位置列表
        """
    lines_list = []
    for i in range(img.shape[0]):  # 遍历图像的每一行
        if np.all(img[i, :] <= [50, 50, 50]):  # 判断该行是否为黑色行，这里设定阈值为 [50, 50, 50]
            # 求该行的像素均值
            mean = np.mean(img[i, :])
            if mean <= 120:  # 如果像素均值小于等于 120，则认为该行是黑色的
                lines_list.append(i)
                # print(f"分界线位置：{i}, 像素均值：{mean}", end="\n\n")
    return lines_list


# def split_img(img):
#     """
#     定义split_img函数，用于将图像分割并保存
#     无返回值
#     """
#     img_width = find_verticalline(img)  # 返回图像的宽度
#     n = 0  # 用于计数分割得到的图像数
#     for i in range(0, img.shape[1], img_width + 1):  # 遍历 img 的每一列
#         image = img[:, i: i + img_width]
#         n += 1
#         file_path = os.path.join(save_path, f"image_{n}.PNG")
#         cv.imwrite(file_path, image)  # 保存图片 无损压缩格式 PNG

def split_num(img):
    """
    定义split_num函数，用于分割数字并保存
    返回数字
    """
    # 将彩色图像转化为灰度图像
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 二值化处理，你可以根据需要调整阈值
    _, thresh = cv.threshold(img_gray, 128, 255, cv.THRESH_BINARY_INV)
    # 查找轮廓
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # 对轮廓进行排序，以便从左到右处理数字（可选）
    contours = sorted(contours, key=lambda x: cv.boundingRect(x)[0])

    # 用于存储识别出的数字字符串
    recognized_digits = []

    # 遍历每个轮廓，并保存每个数字的图片
    for i, contour in enumerate(contours):
        x, y, w, h = cv.boundingRect(contour)
        digit = thresh[y:y + h, x:x + w]
        if digit.shape[0] < 5:  # 小数点的轮廓太小，跳过
            break
        num_index = number_processing.num_list.index(digit.tolist())
        if num_index // 10 == 1:
            num_index = num_index % 10
        # if num_index//10==0:
        recognized_digits.append(str(num_index))

    return int("".join(recognized_digits))


"""
对于雷达数据图，数据标注是左边大右边小为正向
输入参数：原始图片
"""


def save_image(image, filename, save_path):
    """
    保存图像文件，并更新最后保存的文件路径
    :param image: 要保存的图像
    :param filename: 保存的文件名
    :param save_path: 保存路径
    """
    # global last_file_path
    file_path = os.path.join(save_path, filename)
    cv.imwrite(file_path, image)  # 保存图片，无损压缩格式 PNG
    # last_file_path = file_path


def process_images(data, headnum, tailnum, img_width, save_path):
    """
    根据给定条件处理和保存图像
    :param data: 包含图像数据的数组
    :param headnum: 用于命名文件的头部编号
    :param tailnum: 用于命名文件的尾部编号
    :param img_width: 图像的宽度
    :param save_path: 保存路径
    """
    # global last_file_path
    # last_file_path = None
    images_list = []
    n = 0

    if headnum < tailnum:
        for i in range(0, data.shape[1], img_width + 1):  # 遍历数据的每一列
            image = data[:, i: i + img_width]
            n += 1
            filename = f"image_{headnum + n * 5 - 5}.PNG"
            save_image(image, filename, save_path)
            images_list.append(image)
    else:
        for i in range(0, data.shape[1], img_width + 1):  # 遍历数据的每一列
            image = data[:, data.shape[1] - i - img_width: data.shape[1] - i]
            n += 1
            filename = f"image_{tailnum + n * 5 - 5}.PNG"
            save_image(image, filename, save_path)
            images_list.append(image)

    # if last_file_path is not None:
    #     img = cv.imread(last_file_path, cv.IMREAD_COLOR)  # 读取图像，三通道彩色图
    #     print(f"共{n}张图片", n)
    #     cv_info("图片格式", img)  # 假设 cv_info 是一个用于显示图像信息的函数
    # else:
    #     print("没有生成任何分割图片")
    return images_list


def tailnum_revise(num):
    """
    函数是为了将刻度为2的样本处理成刻度为1的样本，后续函数都是针对一刻度为1的样本实现
    :param num:
    :return num:
    """
    # if num%10==0:
    #     num=num/10
    if num % 10 == 2:
        num = num - 2
    elif num % 10 == 1:
        num = num - 1
    elif num % 10 == 6:
        num -= 1
    elif num % 10 == 9:
        num += 1
    return num


def compute_horizontal_resolution(head, tail, data):
    """
    :param head: 首段数据
    :param tail: 尾端数据
    :param data: 输入原图片
    :return: 返回水平分辨率
    """
    if head > tail:
        horiontal_res = (head - tail) / (data.shape[1] - 2 - 64)
    else:
        horiontal_res = (tail - head) / (data.shape[1] - 2 - 64)
    return horiontal_res


def get_tailnum(img):
    """
    定义split_num函数，用于分割数字并保存
    返回数字
    """
    # 将彩色图像转化为灰度图像
    img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    # 二值化处理，你可以根据需要调整阈值
    _, thresh = cv.threshold(img_gray, 128, 255, cv.THRESH_BINARY_INV)
    # 查找轮廓
    contours, _ = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    # 对轮廓进行排序，以便从左到右处理数字（可选）
    contours = sorted(contours, key=lambda x: cv.boundingRect(x)[0])

    # 用于存储识别出的数字字符串
    recognized_digits = []

    # 遍历每个轮廓，并保存每个数字的图片
    for i, contour in enumerate(contours):
        x, y, w, h = cv.boundingRect(contour)
        digit = thresh[y:y + h, x:x + w]
        # print(f"第{i+1}个数字的尺寸：{digit.shape[0]}")
        if digit.shape[0] < 5:  # 小数点的轮廓太小，跳过
            continue
        # if len(recognized_digits) == 3:
        #     recognized_digits=[]
        num_index = number_processing.num_list.index(digit.tolist())
        if num_index // 10 == 1:
            num_index = num_index % 10
        recognized_digits.append(str(num_index))
    length = len(recognized_digits)
    tail_num_list = recognized_digits[::(length // 3)]
    # print(tail_num_list)
    tail_num = int("".join(tail_num_list))
    tail_num = tail_num / 100
    return tail_num


def find_black_horizontal_lines(img):
    """
    寻找图片中的所有黑色水平线
    返回所有黑线的行位置列表
    """
    lines_list = []
    for i in range(img.shape[0]):  # 遍历图像的每一行
        if np.all(img[i, :] <= [50, 50, 50]):  # 判断该行是否为黑色行，这里设定阈值为 [50, 50, 50]
            # 求该行的像素均值
            mean = np.mean(img[i, :])
            if mean <= 120:  # 如果像素均值小于等于 120，则认为该行是黑色的
                lines_list.append(i)
                # print(f"分界线位置：{i}, 像素均值：{mean}", end="\n\n")
    return lines_list


def compute_vertical_resolution(tail_num, line_list):
    """
    :param tail_num: get_tailnum函数得到的尾端数据
    :param line_list: 黑线读取的List输入
    :return:
    """
    vertical_resolution = tail_num / (line_list[-1] - line_list[0])
    return vertical_resolution


def compute_horizontal_resolution(head, tail, data):
    """
    计算水平分辨率
    :param head: 区段开始数据
    :param tail: 区段结束数据
    :param data: 输入原图片
    :return: 返回水平分辨率
    """
    if int(head) > int(tail):
        horiontal_res = (int(head) - int(tail)) / (data.shape[1] - 2 - 64)
    else:
        horiontal_res = (int(tail) - int(head)) / (data.shape[1] - 2 - 64)
    return horiontal_res
