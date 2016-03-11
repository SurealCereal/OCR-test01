# coding=UTF-8

import os
from collections import namedtuple
from math import sqrt
from typing import List

from cereal.Bitmap import RGB, Bitmap

Score = namedtuple('Score', 'character value')


class Glyph(object):
    def __init__(self, character: str, bitmap: Bitmap):
        self.character = character
        self.width = bitmap.width
        self.height = bitmap.height
        self.pixelsPerRow = []   # Horizontal
        self.pixelsPerLine = []  # Vertical (columns)

        offset = 0
        for row in range(bitmap.height):
            pixelsInRow = 0
            for col in range(bitmap.width):
                pixel = bitmap.pixels[offset + col]  # type: RGB
                if pixel.r == 255 and pixel.g == 255 and pixel.b == 255:
                    pixelsInRow += 1
            self.pixelsPerRow.append(pixelsInRow)
            offset += bitmap.width

        for col in range(bitmap.width):
            pixelsInCol = 0
            offset = 0
            for row in range(bitmap.height):
                pixel = bitmap.pixels[offset + col]  # type: RGB
                if pixel.r == 255 and pixel.g == 255 and pixel.b == 255:
                    pixelsInCol += 1
                offset += bitmap.width
            self.pixelsPerLine.append(pixelsInCol)

    def compare(self, glyph: 'Glyph') -> float:
        pixelsPerRowCorrelation = Glyph.linearCorrelationCoefficient(self.pixelsPerRow, glyph.pixelsPerRow)
        pixelsPerLineCorrelation = Glyph.linearCorrelationCoefficient(self.pixelsPerLine, glyph.pixelsPerLine)
        return (pixelsPerRowCorrelation + pixelsPerLineCorrelation) / 2

    """ Calculate the correlation between two 1D numeric lists.  They are expected to have the same number of elements.
        See https://en.wikipedia.org/wiki/Pearson_product-moment_correlation_coefficient#For_a_sample
        and http://mathbits.com/MathBits/TISection/Statistics2/correlation.htm """
    @staticmethod
    def linearCorrelationCoefficient(ints1: List[int], ints2: List[int]) -> float:
        n = len(ints1)
        x_y = 0
        xSum = 0
        ySum = 0

        x2sum = 0
        y2sum = 0

        for it in range(n):
            ix = ints1[it]
            iy = ints2[it]
            x_y += ix * iy
            xSum += ix
            ySum += iy
            x2sum += ix * ix
            y2sum += iy * iy

        dividend = n*x_y - xSum*ySum
        divisor = sqrt(n*x2sum - xSum*xSum) * sqrt(n*y2sum - ySum*ySum)

        return dividend / divisor


class PotentialGlyph(Glyph):

    def __init__(self, character: str, bitmap: Bitmap):
        super().__init__(character, bitmap)
        self.top = 0
        self.left = 0
        self.bottom = 0
        self.right = 0


class OCR(object):

    def __init__(self):
        self.image = []
        self.glyphs = {}
        self.charMatchThreshold = 0.75

    def loadCharset(self, directory: str):
        files = os.listdir(directory)
        for filename in files:
            if filename.endswith('.bmp'):
                self.addGlyph(directory, filename)

    def addGlyph(self, directory: str, filename: str):
        # Get the file name without [the extension including .]
        character = filename.rstrip('.bmp')
        path = directory + os.sep + filename
        print("\nLoading \"%s\" - Glyph for character \"%c\"" % (path, character))
        bmp = Bitmap(path)
        # Create a glyph for the bitmap
        glyph = Glyph(character, bmp)
        self.glyphs[character] = glyph

        # print the glyph
        offset = 0
        for row in range(0, bmp.height):
            rowStr = ""
            for col in range(0, bmp.width):
                pixel = bmp.pixels[offset + col]  # type: RGB
                if pixel.r == 255 and pixel.g == 255 and pixel.b == 255:
                    rowStr += '■'
                else:
                    rowStr += '□'
            print(rowStr)
            offset += bmp.width

    # Extract character strings from an image.
    def process(self, imagePath: str) -> PotentialGlyph:
        # lines = [[]]

        print('\nProcessing %s' % imagePath)
        bmp = Bitmap(imagePath)

        """ De-speckle - remove positive and negative spots, smoothing edges. """

        """ De-skew - make lines of text perfectly horizontal or vertical (Japanese). """

        """ Binarize Image - Convert to gray-scale and then 1-bit. """

        """ Fill small holes/cracks that may arrise during binarization. """

        """ Line-removal - Remove non-glyph boxes and lines.  """

        """ Character isolation or "segmentation" """

        """ Normalise aspect ratio and scale """

        """ Recognize characters, and classify confidence levels for each.
            There may be multiple interpretations for each, so store them for later. """

        pg = self.processCharacters(bmp)

        """ Recognize words based on geometric parameters. """

        """ Recognize sentences. """

        """ Deal with characters that had multiple potential interpretations.
            See what makes most sense in the context of the word and sentence. """

        return pg

    def processCharacters(self, bmp: Bitmap) -> PotentialGlyph:
        # Create a glyph for the bitmap
        pg = PotentialGlyph('', bmp)

        # Compare this potential character with each known glyph
        scores = []  # type: List[Score]
        for char, glyph in self.glyphs.items():
            score = Score(char, glyph.compare(pg))
            scores.append(score)
        scores.sort(key=lambda aScore: aScore.value, reverse=True)

        if len(scores) > 0 and scores[0].value > self.charMatchThreshold:
            pg.character = scores[0].character
        else:
            pg.character = ''

        print('Found "%s" in the image.' % pg.character)

        return pg
