
import argparse
import os

import numpy
from skimage import io, color


parser = argparse.ArgumentParser()
parser.add_argument('output_path')
parser.add_argument('images', nargs='+')

to_fix = [
    "images/resized/IMG_2648.jpg",
    "images/resized/IMG_2728.jpg",
    "images/resized/IMG_2761.jpg",
    "images/resized/IMG_2782.jpg",
    "images/resized/IMG_2800.jpg",
    "images/resized/IMG_2816.jpg",
    "images/resized/IMG_2832.jpg",
    "images/resized/IMG_2845.jpg",
]


lab_l_bins = numpy.arange(0, 100)
lab_l_bins = numpy.append(lab_l_bins, 100)

hsv_v_bins = numpy.arange(0, 1, 0.0001)
hsv_v_bins = numpy.append(hsv_v_bins, 1)


def get_hsv_value_component(img):
    hsv = color.rgb2hsv(img)
    return hsv[:, :, 2]

def replace_hsv_value_component(img, values):
    hsv = color.rgb2hsv(img)
    hsv[:, :, 2] = values
    img = color.hsv2rgb(hsv)
    return img

def get_lab_luminance_component(img):
    lab = color.rgb2lab(img)
    return lab[:, :, 0]

def replace_lab_luminance_component(img, values):
    lab = color.rgb2lab(img)
    lab[:, :, 0] = values
    img = color.lab2rgb(lab)
    return img

def get_cdf(values, bins):
    hist, _ = numpy.histogram(values, bins, density=True)
    cdf = hist.cumsum()
    return cdf


def match(values, source, target, bins):
    v = numpy.interp(values, bins, source)
    return numpy.interp(v, target, bins)


def produce_smoothed_images(get_component, replace_component, bins, output_path, paths):

    start_img = io.imread(paths[0])
    start_cdf = get_cdf(get_component(start_img), bins)

    end_img = io.imread(paths[-1])
    end_cdf = get_cdf(get_component(end_img), bins)

    delta_cdf = end_cdf - start_cdf

    for i, path in enumerate(paths[1:-1]):
        percentage = i / len(paths[1:-1])
        target_cdf = start_cdf + (delta_cdf * percentage)

        img = io.imread(path)
        values = get_component(img)
        cdf = get_cdf(values, bins)

        # In order to match the length of "bins" for the interpolation below
        # we prepend a 0
        target_cdf = numpy.insert(target_cdf, 0, 0)
        cdf = numpy.insert(cdf, 0, 0)

        matched = match(values, cdf, target_cdf, bins)
        matched = matched.reshape(values.shape)

        img = replace_component(img, matched)

        result_path = os.path.join(output_path, os.path.basename(path))
        io.imsave(result_path, img)
        print('Done with', result_path)


if __name__ == '__main__':
    args = parser.parse_args()
    paths = list(args.images)

    for path in to_fix:
        i = paths.index(path)
        # produce_smoothed_images(get_hsv_value_component,
        #                         replace_hsv_value_component,
        #                         hsv_v_bins,
        #                         args.output_path,
        #                         paths[i - 1:i + 8])
        produce_smoothed_images(get_lab_luminance_component,
                                replace_lab_luminance_component,
                                lab_l_bins,
                                args.output_path,
                                paths[i - 1:i + 8])
