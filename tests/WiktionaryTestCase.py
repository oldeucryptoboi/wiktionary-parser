import os

from compat import File


class WiktionaryTestCase:
    """ Abstract test case for PyWKTL. """

    RESOURCE_PATH = os.path.join(os.getcwd(), "resources")

    workDir = None

    # noinspection PyMethodMayBeStatic
    def getName(self):
        return ""

    def setUp(self):  # throws Exception
        # super().setUp()
        self.workDir = File(os.path.join(os.getcwd(), "target/test-output/"), self.__class__.__name__ + "_" + self.getName())
        self.deleteDirectory(self.workDir)
        self.workDir.mkdir()

    def tearDown(self):  # throws Exception
        self.deleteDirectory(self.workDir)
        # super().tearDown()

    @classmethod
    def deleteDirectory(cls, path):
        if path.exists():
            files = path.listFiles()
            for file in files:
                if file.isDirectory():
                    if not cls.deleteDirectory(file):
                        print("Unable to delete dir: " + file)
                else:
                    if not file.delete():
                        print("Unable to delete file: " + file)
        return path.delete()

    def assertTrue(self):
        pass

    def assertFals(self):
        pass

    def assertEqual(self):
        pass


