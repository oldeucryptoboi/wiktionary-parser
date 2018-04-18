from compat import InputStream
import bz2


class BZip2InputStream(InputStream):
    """ An input stream which keeps decompressing data from the file / stream until
        it hits EOF. Useful for decoding files which contain multiple bz2 streams. """

    def __init__(self, file):  # throws FileNotFoundException :
        self.underlying = bz2.BZ2File(file.filepath, 'rb')

    def __enter__(self):
        return self

    def __exit__(self, type_, value, traceback):
        self.underlying.close()
        pass

    def readline(self):  # throws IOException :
        line = None
        try:
            line = self.underlying.readline()
        except Exception:
            self.underlying = None
        finally:
            return line

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
