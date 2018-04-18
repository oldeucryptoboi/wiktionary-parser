import unittest

from compat import *
import hashlib

from parser import BZip2InputStream


class TestBZip2InputStream(unittest.TestCase):

    def testConsumeWholeStream(self):  # throws Exception
        path = os.path.join(os.getcwd(), "resources")
        name = "enwiktionary-20150224-pages-articles-multistream.xml.bz2"
        hash_md5 = hashlib.md5()
        with BZip2InputStream(File(path, name)) as stream:
            for chunk in iter(lambda: stream.read(4096), b""):
                hash_md5.update(chunk)
        signature = hash_md5.hexdigest()

        # self.assertEqual(1800617, count)
        self.assertEqual("bde6a439065407c9c74c83b1f2f97520", signature)
