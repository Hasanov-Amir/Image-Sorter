import numpy as np
from sklearn.cluster import KMeans


def get_dominant_color(image, k=4):
    image = np.array(image)
    pixels = image.reshape(-1, 3)
    kmeans = KMeans(n_clusters=k)
    kmeans.fit(pixels)
    dominant_color = kmeans.cluster_centers_[np.argmax(np.bincount(kmeans.labels_))]
    return tuple(map(int, dominant_color))


def get_image_orientation(image):
    width, height = image.size
    if width > height:
        return "horizontal"
    else:
        return "vertical"
