import argparse

import numpy
from skimage import io, color
import matplotlib.pyplot as plot


parser = argparse.ArgumentParser()
parser.add_argument('path_a')
parser.add_argument('path_b')


def get_hsv_values(path):
    img = io.imread(path)
    hsv = color.rgb2hsv(img)
    return hsv[:, :, 2].flatten()


def get_lab_luminance_component(path):
    img = io.imread(path)
    lab = color.rgb2lab(img)
    return lab[:, :, 0].flatten()


def open_greyscale(path):
    return io.imread(path, as_grey=True).flatten()


def plot_hists(bins, values_a, values_b):
    f, (ax1, ax2) = plot.subplots(nrows=2, ncols=1, sharex=True, sharey=True)
    ax1.hist(values_a, bins, histtype='stepfilled', cumulative=True, normed=True)
    ax2.hist(values_b, bins, histtype='stepfilled', cumulative=True, normed=True)

    plot.show()


def plot_hsv_value_hist(path_a, path_b):
    values_a = get_hsv_values(path_a)
    values_b = get_hsv_values(path_b)
    plot_hists(1000, values_a, values_b)


def plot_greyscale_hist(path_a, path_b):
    values_a = open_greyscale(path_a)
    values_b = open_greyscale(path_b)
    plot_hists(256, values_a, values_b)





def plot_luminance_hist(path_a, path_b):
    values_a = get_lab_luminance_component(path_a)
    values_b = get_lab_luminance_component(path_b)
    plot_hists(100, values_a, values_b)


if __name__ == '__main__':
    args = parser.parse_args()
    plot_luminance_hist(args.path_a, args.path_b)
    # plot_greyscale_hist(args.path_a, args.path_b)
