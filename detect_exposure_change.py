import argparse
import os

from more_itertools import pairwise
import numpy
from skimage import io, color


parser = argparse.ArgumentParser()
parser.add_argument('images', nargs='+')


def get_hsv_values(path):
    img = io.imread(path)
    hsv = color.rgb2hsv(img)
    values = hsv[:, :, 2].flatten()
    return values

def open_grayscale(path):
    return io.imread(path, as_grey=True)

def mean_hist_delta(path_a, path_b, bins):
    values_a = get_hsv_values(path_a)
    values_b = get_hsv_values(path_b)
    # values_a = open_grayscale(path_a).flatten()
    # values_b = open_grayscale(path_b).flatten()

    hist_a, _ = numpy.histogram(values_a, bins, density=True)
    hist_b, _ = numpy.histogram(values_b, bins, density=True)

    delta = numpy.absolute(hist_b - hist_a)
    return numpy.mean(delta)


if __name__ == '__main__':
    args = parser.parse_args()
    paths = list(args.images)
    bins = 256

    for path_a, path_b in pairwise(paths):
        m = mean_hist_delta(path_a, path_b, bins)
        if m > 0.6:
            print(os.path.basename(path_a), os.path.basename(path_b), m)
