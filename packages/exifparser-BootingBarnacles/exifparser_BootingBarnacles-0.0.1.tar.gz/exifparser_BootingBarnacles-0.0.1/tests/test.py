import unittest
import glob
from src.exifparser.exif import ExifHeaderListParser

def get_valid_images(): return ["images/valid.jpg"]

def get_invalid_images(): return ["images/no_exif.jpg"]


class Test_ExifParserList(unittest.TestCase):
    
    def test_handles_valid_jpg_glob(self):
        files = get_valid_images()
        sut = ExifHeaderListParser(jpgs=files)
        sut.parse()
        self.assertTrue(len(sut.items.items()) == 1)
        
    def test_handles_exception_for_invalid_glob(self):
        files = []
        sut = ExifHeaderListParser(jpgs=files)
        self.assertRaises(Exception, sut.parse)
    
    def test_filename_is_stored_as_key(self):
        files = get_valid_images()
        sut = ExifHeaderListParser(jpgs=files)
        sut.parse()
        first_image_name = glob.glob("images/*.jpg")[0]
        file_image_names = list(sut.items.keys())
        self.assertEqual(first_image_name, file_image_names[0])

    def test_parse_handles_images_without_exif_header(self):
        files = get_invalid_images()
        sut = ExifHeaderListParser(jpgs=files)
        self.assertRaises(Exception, sut.parse)

