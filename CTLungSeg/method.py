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
    pass

def std_filter(image, radius):
    pass

def gamma_correction(image, gamma, image_type='HU'):
    pass