import numpy as np
import CTLungSeg.method


def remove_vessel(image, sigma=2, threshold=8):
    """移除血管"""
    smoothed = CTLungSeg.method.gaussian_filter(image, sigma=sigma)
    vessel = CTLungSeg.method.find_vessel(smoothed)
    vessel_mask = CTLungSeg.method.threshold(image=vessel, upper=4000, lower=threshold, inside=0,
                                             outside=1)  # inside为血管,后续不处理,则设置为0,外部为肺部,后续需要,则设置为1
    return CTLungSeg.method.apply_mask(image=image, mask=vessel_mask, outside_value=-1000)


def kmeans_on_subs(image, n_centroids, stopping_criteria, centroids_init, weight=False):
    """子样本kmeans"""
    features = image[0].shape[-1]
    if weight:
        vector = np.asarray([ele[:, :, :, : -1][ele[:, :, :, -1] != 0] for ele in image], dtype=np.ndarray)
    else:
        vector = np.asarray([ele.reshape(-1, features) for ele in image], dtype=np.ndarray)

    ret_centroid = []
    ret_compactness = []

    from tqdm import tqdm
    import cv2
    for ele in tqdm(vector):
        compactness, labels, centroids = cv2.kmeans(ele.astype(np.float32),
                                                    K=n_centroids,
                                                    bestLabels=None,
                                                    criteria=stopping_criteria,
                                                    attempts=10,
                                                    flags=centroids_init)
        ret_centroid.append(centroids)
        ret_compactness.append(compactness)

    return [np.asarray(ret_compactness, dtype=np.float32), np.asarray(ret_centroid, dtype=np.float32)]


def image_labeling(image, centroids, weight=None):
    """按照质心对图像进行标记"""
    if centroids.shape[1] != image.shape[-1]:
        raise Exception(
            f"Nums of image features' channels dose not match nums of centroids' features: {image.shape[-1]}!={centroids.shape[1]}")
    if weight is not None:
        if weight.shape != image.shape[: -1]:
            raise Exception(f"Weight(mask) shape dose not match images' shape: {weight.shape} != {image.shape[: -1]}")

        distances = np.asarray(np.linalg.norm(image[weight != 0] - c, axis=1) for c in centroids)
        weight[weight != 0] = np.argmin(distances, axis=0)
        return weight

    else:
        distances = np.asarray([np.linalg.norm(image - c, axis=3) for c in centroids])
        labels = np.argmin(distances, axis=0)
        return labels
