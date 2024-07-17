import math


def rgb_to_yuv(color):
    R, G, B = color
    Y = 0.299 * R + 0.587 * G + 0.114 * B
    U = 0.492 * (B - Y)
    V = 0.877 * (R - Y)
    return (Y, U, V)


def yuv_distance(color1, color2):
    yuv1 = rgb_to_yuv(color1)
    yuv2 = rgb_to_yuv(color2)
    return math.sqrt(sum((c1 - c2) ** 2 for c1, c2 in zip(yuv1, yuv2)))
