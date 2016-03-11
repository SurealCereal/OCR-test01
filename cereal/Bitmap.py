# coding=UTF-8

import struct
from collections import namedtuple
from math import floor
from typing import List

RGB = namedtuple('RGB', 'r g b')


class Bitmap(object):

    def __init__(self, path: str):
        self.width = 0    # type: int
        self.height = 0   # type: int
        self.bpp = 0      # type: int
        self.pixels = []  # type: List[RGB]

        bmFile = open(path, 'r+b', 0)
        bmBytes = bytearray(bmFile.read())
        """
Structure name 	    Optional 	Size 	    Purpose
Bitmap file header 	No          14 bytes 	To store general information about the bitmap image file.
DIB header 	        No 	        Fixed-size (7 possible sizes)
                                            Detailed information about the bitmap image and the pixel format.
Extra bit masks 	Yes 	    3 or 4 DWORDs[6] (12 or 16 bytes)
                                            To define the pixel format 	Present only in case the DIB header is the
                                            BITMAPINFOHEADER & the Compression Method member is set to either
                                            BI_BITFIELDS or BI_ALPHABITFIELDS.
Color table 	    Semi 	    Variable    To define colors used by the bitmap image data (Pixel array)
                                            Mandatory for color depths ≤ 8 bits.
Gap1 	            Yes 	    Variable	Structure alignment
                                            An artifact of the File offset to Pixel array in the Bitmap file header
Pixel array 	    No 	        Variable 	To define the actual values of the pixels.
                                            The pixel format is defined by the DIB header or Extra bit masks.
                                            Each row in the Pixel array is padded to a multiple of 4 bytes in size

        Read Bitmap File header - 14 bytes
        Offset (hex), Offset (dec), Size (bytes), Purpose
        00 	0   2 Bytes - Used to identify the BMP and DIB file is 0x42 0x4D in hexadecimal, same as BM in ASCII.
        02 	2   4 bytes - Size of the BMP file in bytes
        06 	6   2 bytes - Reserved
        08 	8   2 bytes - Reserved
        0A 	10  4 bytes - Offset, i.e. starting address, of the byte where the bitmap image data (pixel array) can be found.
        """
        magic, fileSize, res1, res2, pixelsAddr = struct.unpack_from("<2sIHHI", bmBytes, 0)
        # print('magic: %s, fileSize: %d, res1: %d, res2: %d, pixelsOffset: %d' %
        #      (magic, fileSize, res1, res2, pixelsAddr))
        """
        Read  DIB header - expects BITMAPINFOHEADER, i.e for a standard BMP file:
        Offset (hex), Offset (dec), Size (bytes), Purpose
        0E 	14 	4 	Size of this header (40 bytes)
        12 	18 	4 	Bitmap width in pixels (signed integer)
        16 	22 	4 	Bitmap height in pixels (signed integer)
        1A 	26 	2 	Number of color planes (must be 1)
        1C 	28 	2 	Number of bits per pixel, which is the color depth of the image. Typically 1, 4, 8, 16, 24 or 32.
        1E 	30 	4 	Compression method. See the next table for a list of possible values
        22 	34 	4 	Image size. This is the size of the raw bitmap data; a dummy 0 can be given for BI_RGB bitmaps.
        26 	38 	4 	Horizontal resolution of the image. (pixel per meter, signed integer)
        2A 	42 	4 	Vertical resolution of the image. (pixel per meter, signed integer)
        2E 	46 	4 	Number of colors in the color palette, or 0 to default to 2ⁿ
        32 	50 	4 	Number of important colors used, or 0 when every color is important; generally ignored

        Compression Methods:
        Value, 	Identifier, 	Compression method 	Comments
        0 	    BI_RGB          none 	            Packed RGB pixels
        1 	    BI_RLE8 	    RLE 8-bit/pixel 	Can be used only with 8-bit/pixel bitmaps
        2 	    BI_RLE4 	    RLE 4-bit/pixel 	Can be used only with 4-bit/pixel bitmaps
        """
        dibHeaderSize, self.width, self.height, planes, self.bpp, compressionMethod, imageSize, hRes, yRes, \
        paletteSize, importantColors = struct.unpack_from("<IiiHHIIIIII", bmBytes, 14)
        # print('dibHeaderSize: %d' % dibHeaderSize)
        print('width: %d, height: %d, bpp: %d, compressionMethod: %d' %
              (self.width, self.height, self.bpp, compressionMethod))
        # print('planes: %d, imageSize: %d, hRes: %d, yRes: %d' % (planes, imageSize, hRes, yRes))
        # print('paletteSize: %d, importantColors: %d' % (paletteSize, importantColors))

        """
        The bits representing the bitmap pixels are packed in rows.
        The size of each row is rounded up to a multiple of 4 bytes (a 32-bit DWORD) by padding.
        For images with height > 1, multiple padded rows are stored consecutively, forming a Pixel Array.
        The total number of bytes necessary to store one row of pixels can be calculated as:
            rowSize = floor((bpp * width + 31) / 32) * 4

        The total amount of bytes necessary to store an array of pixels in an n bits per pixel (bpp) image,
        with 2ⁿ colors, can be calculated by accounting for the effect of rounding up the size of each row
        to a multiple of a 4 bytes, as follows:
            bytes = rowSize * |height|

        PEL order is BGR
        """
        rowSize = int(floor((self.bpp * self.width + 31) / 32) * 4)
        padding = int(rowSize - ((self.bpp * self.width) / 8))
        rawRowSize = rowSize-padding
        numBytes = rowSize * abs(self.height)

        print("rowSize: %d, padding: %d, numBytes: %d" % (rowSize, padding, numBytes))

        # del self.pixels[:]
        self.pixels = []
        offset = pixelsAddr + (self.height*rowSize)
        rowFormat = "<%dB" % rawRowSize
        for rowIndex in range(self.height-1, -1, -1):
            offset -= rowSize
            row = struct.unpack_from(rowFormat, bmBytes, offset)
            for px in range(0, rawRowSize, 3):
                self.pixels.append(RGB(row[px+2], row[px+1], row[px]))
