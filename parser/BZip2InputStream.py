from compat import InputStream
import bz2


class BZip2InputStream(InputStream):
    """ An input stream which keeps decompressing data from the file / stream until
        it hits EOF. Useful for decoding files which contain multiple bz2 streams. """

    def __init__(self, file):  # throws FileNotFoundException :
        self.underlying = bz2.BZ2File(file.filepath, 'r')

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.underlying.close()
        pass

    def __next__(self):
        line = self.underlying.readline().decode('utf-8').rstrip('\n')
        if not line:
            self.underlying = None
            raise StopIteration
        return line

    def __iter__(self):
        return self

    def readLine(self):  # throws IOException :
        return self

    def read(self, size=1):  # throws IOException :
        byte = None
        try:
            byte = self.underlying.read(size)
        except Exception:
            self.underlying = None
            return byte
        finally:
            return byte

    def close(self):  # throws IOException :
        if self.underlying is not None:
            self.underlying.close()
            self.underlying = None
