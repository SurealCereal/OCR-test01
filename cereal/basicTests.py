import unittest

from cereal.OCR import OCR


class BasicTests(unittest.TestCase):
    ocr = None

    def __init__(self, methodName='runTest'):
        super().__init__(methodName)
        if not (type(BasicTests.ocr) is OCR):
            BasicTests.ocr = OCR()  # type: OCR
            BasicTests.ocr.loadCharset('../data/ocr-a')

    def test_OCR_0(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x0.bmp')
        self.assertEqual(pg.character, '0')

    def test_OCR_1(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x1.bmp')
        self.assertEqual(pg.character, '1')

    def test_OCR_2(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x2.bmp')
        self.assertEqual(pg.character, '2')

    def test_OCR_3(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x3.bmp')
        self.assertEqual(pg.character, '3')

    def test_OCR_4(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x4.bmp')
        self.assertEqual(pg.character, '4')

    def test_OCR_5(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x5.bmp')
        self.assertEqual(pg.character, '5')

    def test_OCR_6(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x6.bmp')
        self.assertEqual(pg.character, '6')

    def test_OCR_7(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x7.bmp')
        self.assertEqual(pg.character, '7')

    def test_OCR_8(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x8.bmp')
        self.assertEqual(pg.character, '8')

    def test_OCR_9(self):
        pg = BasicTests.ocr.process('../data/test_chars-ocr-a/x9.bmp')
        self.assertEqual(pg.character, '9')

if __name__ == '__main__':
    unittest.main()
