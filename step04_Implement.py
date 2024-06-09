from lungmask.mask import apply
import SimpleITK as sitk
import numpy as np

from CTLungSeg.utils import read_image
from CTLungSeg.method import apply_mask
from CTLungSeg.segmentation import remove_vessel
from CTLungSeg.utils import shift_and_threshold
from CTLungSeg.utils import normalize
from CTLungSeg.method import adaptive_histogram_equalization, median_filter, std_filter, gamma_correction, threshold

import cv2
from CTLungSeg.utils import shuffle_and_split
from CTLungSeg.segmentation import kmeans_on_subs
from CTLungSeg.segmentation import image_labeling

import matplotlib.pyplot as plt

# load data
img01 = read_image('')
img02 = read_image('')
img03 = read_image('')


# lung extraction
def lung_extraction(img):
    # 应用lungmask模型
    lung_mask = apply(img)
    # 二值化目标区域
    lung_mask = (lung_mask != 0).astype(np.uint8)
    # 转为sitk图像文件,供sitk的mask_filter使用
    lung_mask = sitk.GetImageFromArray(lung_mask)
    # 原图信息复制
    lung_mask.CopyInformation(img)
    # 应用掩膜到原图
    masked = apply_mask(image=img, mask=lung_mask, outside_value=-1000)
    # 移除肺部血管
    vessel_removed = remove_vessel(image=masked)
    # 平移 + 剪裁
    result = shift_and_threshold(image=vessel_removed)

    return result


lung01 = lung_extraction(img01)
lung02 = lung_extraction(img02)
lung03 = lung_extraction(img03)


# feature computation
def computation_filter(img):
    # 一系列滤波器处理
    ahe = normalize(adaptive_histogram_equalization(image=img, radius=2))
    med = normalize(median_filter(image=img, radius=3))
    std = normalize(std_filter(image=img, radius=3))
    gamma = normalize(gamma_correction(image=img, gamma=1.5))
    mask = threshold(image=img, upper=4000, lower=1)

    # 转为ndarray
    ahe = sitk.GetArrayFromImage(ahe)
    med = sitk.GetArrayFromImage(med)
    std = sitk.GetArrayFromImage(std)
    gamma = sitk.GetArrayFromImage(gamma)
    mask = sitk.GetArrayFromImage(mask)

    # 堆叠
    stack = np.stack([ahe, med, std, gamma, mask], axis=-1)
    return stack


feature01 = computation_filter(lung01)
feature02 = computation_filter(lung02)
feature03 = computation_filter(lung03)

# train
training_set = np.concatenate((feature01, feature03), axis=0)
stop_criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, .001)

sub_samples = shuffle_and_split(data=training_set, num_of_subs=15)

compactness, centroids = kmeans_on_subs(image=sub_samples,
                                        n_centroids=5,
                                        stopping_criteria=stop_criteria,
                                        centroids_init=cv2.KMEANS_PP_CENTERS,
                                        weight=True
                                        )
best_centroids = centroids[np.argmin(compactness)]
best_centroids = best_centroids[best_centroids[:, 0].argsort()]

# labeling
labeled_img = image_labeling(image=feature02[:, :, :, : -1], centroids=best_centroids, weight=feature02[:, :, :, -1])

# display labeled img
plt.imshow(labeled_img[150], cmap='gray')
plt.show()

# display ggo area (index=3)
labeled_img_idx3 = (labeled_img == 3).astype(np.uint8)
ground_truth = read_image('')
ground_truth = sitk.GetArrayFromImage(ground_truth)

fig, ax = plt.subplot(nrows=1, ncols=2, figsize=(10, 10))
ax[0].axis('off')
ax[0].imshow(labeled_img_idx3[150], cmap='gray')
ax[0].set_title('Segmentation Result', fontsize=20)

ax[1].axis('off')
ax[1].imshow(ground_truth[150] == 3, cmap='gray')
ax[1].set_title('Ground Truth', fontsize=20)
