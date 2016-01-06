import argparse
import os

import numpy
from scipy import interpolate
from skimage import io, img_as_ubyte, exposure, color


parser = argparse.ArgumentParser()
parser.add_argument('images', nargs='+')


def ref_curve(path, bins):
    img = io.imread(path)
    hsv = color.rgb2hsv(img)
    vals = hsv[:, :, 2]

    hist, bins = numpy.histogram(vals, bins, density=True)
    cdf = hist.cumsum()

    def d(inp):
        b = numpy.digitize(inp, cdf)
        return numpy.array([bins[i] for i in b])

    return d


if __name__ == '__main__':
    args = parser.parse_args()
    paths = list(args.images)

    #bins = numpy.arange(0, 1, 0.01)
    bins = 256
    ref = ref_curve(paths[0], bins)

    for path in paths:
        print(path)

        img = io.imread(path)
        hsv = color.rgb2hsv(img)

        vals = hsv[:, :, 2].flatten()
        vhist, vbins = numpy.histogram(vals, bins, density=True)
        vcdf = vhist.cumsum()

        a = numpy.interp(vals, vbins[:-1], vcdf)

        mapped = ref(a).reshape(hsv[:, :, 2].shape)
        hsv[:, :, 2] = mapped

        copy_path = os.path.join(os.path.dirname(path), 'corrected', os.path.basename(path))
        img = color.hsv2rgb(hsv)
        io.imsave(copy_path, img)
