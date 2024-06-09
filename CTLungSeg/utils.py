import os.path

import SimpleITK as sitk
import numpy as np


def _read_image(path):
    """定义sitk图片读取器(比较与sitk.ReadImage()区别)"""
    reader = sitk.ImageFileReader()
    reader.SetFileName(path)
    return reader


def _read_image_series(path):
    """定义sitk图片组读取器"""
    reader = sitk.ImageSeriesReader()
    names = reader.GetGDCMSeriesFileNames(path)  # 设置文件序列名为源文件名
    reader.SetFileNames(names)
    return reader


def read_image(path):
    """读取图片/图片组"""
    if os.path.exists(path):
        if os.path.isfile(path):
            reader = _read_image(path)
        elif os.path.isdir(path):
            reader = _read_image_series(path)

        img = reader.Execute()
    else:
        raise FileNotFoundError(f'{path} not exists')

    return img


def shift_and_threshold(image):
    """将HU值整体平移(shift)直至下限为0,再将峰值大于+2048的部分截断(threshold)"""
    shift = sitk.ShiftScale(image, 1000, 1.0)  # 1000:偏移量,1.0:缩放比例
    shift_threshold = sitk.Threshold(image1=shift, lower=0, upper=2048, outsideValue=0)
    return shift_threshold


def normalize(image):
    """归一化"""
    statistics = sitk.StatisticsImageFilter()  # 统计信息过滤器
    statistics.Execute(image)
    if np.isclose(statistics.GetSigma(), 0):  # 图像标准差是否接近0(单色图),是则无法归一化
        raise ZeroDivisionError('Cannot normalize image with zero sigma')
    normalizer = sitk.NormalizeImageFilter()
    return normalizer.Execute(image)


def shuffle_and_split(data, num_of_subs):
    """打乱且分组"""
    np.random.shuffle(data)
    array_list = np.array_split(data, num_of_subs)
    return np.array(array_list, dtype=np.ndarray)
