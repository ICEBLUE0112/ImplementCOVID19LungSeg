import SimpleITK as sitk


def apply_mask(image, mask, masking_value=0, outside_value=-1500):
    """将掩膜覆盖至原图"""
    mask_filter = sitk.MaskImageFilter()  # 掩膜过滤器
    mask_filter.SetMaskingValue(masking_value)  # 目标区域
    mask_filter.SetOutsideValue(outside_value)  # 非目标区域
    return mask_filter.Execute(image, mask)


def gaussian_filter(image, sigma=1.):
    """平滑图像"""
    filter = sitk.SmoothingRecursiveGaussianImageFilter()
    filter.SetSigma(sigma)
    return filter.Execute(image)


def find_vessel(image):
    """寻找血管(一维特征)"""
    filter = sitk.ObjectnessMeasureImageFilter()
    filter.SetObjectDimension(1)
    return filter.Execute(image)


def threshold(image, upper, lower, inside=1, outside=0):
    """区间阈值"""
    filter = sitk.BinaryThresholdImageFilter()
    filter.SetLowerThreshold(lower)
    filter.SetUpperThreshold(upper)
    filter.SetInsideValue(inside)
    filter.SetOutsideValue(outside)
    return filter.Execute(image)


def adaptive_histogram_equalization(image, radius):
    """自适应直方图均衡化"""
    filter = sitk.AdaptiveHistogramEqualizationImageFilter()
    filter.SetAlpha(1)
    filter.SetBeta(1)
    filter.SetRadius(radius)
    return filter.Execute(image)


def median_filter(image, radius):
    """中值滤波,去除椒盐噪音"""
    if radius <= 0:
        raise ValueError('radius must be greater or equal than 1')
    filter = sitk.MedianImageFilter()
    filter.SetRadius(int(radius))
    return filter.Execute(image)


def std_filter(image, radius):
    """标准差滤波,平滑图像"""
    if radius <= 0:
        raise ValueError('radius must be greater or equal than 1')
    filter = sitk.NoiseImageFilter()
    filter.SetRadius(int(radius))
    return filter.Execute(image)


def cast_image(image, target_type):
    """图像类型转换"""
    filter = sitk.CastImageFilter()
    filter.SetOutputPixelType(target_type)
    return filter.Execute(image)


def gamma_correction(image, gamma=1.0, image_type='HU'):
    """伽马校正"""
    bounding_values = {'uint8': [0, 255],
                       'uint16': [0, 2 ** 16],
                       'HU': [0, 2 ** 12]
                       }
    image_types = {'uint8': sitk.sitkUInt8,
                   'uint16': sitk.sitkUInt16,
                   'HU': sitk.sitkUInt16}
    if gamma == 0:
        raise Exception('gamma value cannot be zero')
    if image_type not in ['uint8', 'uint16', 'HU']:
        raise Exception(f'image type {image_type} is not supported')

    image = cast_image(image, sitk.sitkFloat32)
    power_filter = sitk.PowImageFilter()
    inverse_gamma = 1.0 / gamma
    output = power_filter.Execute(image, inverse_gamma)
    cur_bound = bounding_values[image_type]
    out = sitk.Threshold(image1=output, lower=cur_bound[0], upper=cur_bound[1], outsideValue=cur_bound[1])
    out = sitk.Cast(out, image_types[image_type])
    return out
