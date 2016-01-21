import argparse
import os

from more_itertools import pairwise
import numpy
from scipy import interpolate
from skimage import io, img_as_ubyte, exposure, color
import matplotlib.pyplot as plot


parser = argparse.ArgumentParser()
parser.add_argument('output_path')
parser.add_argument('images', nargs='+')


def ref_curve(path, bins):
    img = io.imread(path)
#    img = exposure.equalize_hist(img)
    hsv = color.rgb2hsv(img)
    vals = hsv[:, :, 2]

    hist, bins = numpy.histogram(vals, bins, density=True)
    cdf = hist.cumsum()

    def d(inp):
        b = numpy.digitize(inp, cdf)
        return numpy.array([bins[i] for i in b])

    return d


def match(img, ref, bins):
    hsv = color.rgb2hsv(img)

    vals = hsv[:, :, 2].flatten()
    vhist, vbins = numpy.histogram(vals, bins, density=True)
    vcdf = vhist.cumsum()

    a = numpy.interp(vals, vbins[:-1], vcdf)

    mapped = ref(a).reshape(hsv[:, :, 2].shape)
    hsv[:, :, 2] = mapped
    ret_img = color.hsv2rgb(hsv)
    return ret_img


def use_first(paths, bins):
    ref = ref_curve(paths[0], bins)

    for path in paths:
        print(path)
        img = io.imread(path)
        yield match(img, ref, bins)


def use_pairs(paths, bins):
    is_first = True

    for path_a, path_b in pairwise(paths):
        if is_first:
            is_first = False
            yield io.imread(path_a)

        else:
            ref = ref_curve(path_a, bins)
            img_b = io.imread(path_b)
            yield match(img_b, ref, bins)


def deflicker():
    #bins = numpy.arange(0, 1, 0.01)
    bins = 256

    for path, img in zip(paths, use_first(paths, bins)):
        output_path = os.path.join(output_directory, os.path.basename(path))
        io.imsave(output_path, img)
