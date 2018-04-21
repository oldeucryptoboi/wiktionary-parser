from collections import OrderedDict

from configparser import ConfigParser
from errors import NoSuchElementException, IOException

import os
import io


DEBUG = False


class Long:

    @classmethod
    def parseLong(cls, str):
        return int(str)


class String:
    pass


class Object:

    @classmethod
    def getResourceAsStream(cls, filepath):
        return filepath


class File:

    def __init__(self, path, name):
        self.filename = name
        self.filepath = os.path.join(path, name)

    def getName(self):
        return self.filename

    def exists(self):
        return os.path.exists(self.filepath)

    def isDirectory(self):
        return os.path.isdir(self.filepath)

    def listFiles(self):
        return os.listdir(self.filepath)

    def delete(self):
        try:
            os.remove(self.filepath)
        except OSError:
            try:
                os.rmdir(self.filepath)
            except OSError:
                return False

        return True

    def getAbsolutePath(self):
        return self.filepath

    def __str__(self):
        return self.filepath

    def mkdirs(self):
        try:
            os.mkdir(self.filepath)
            return True
        except FileExistsError:
            print("File exists!")
        except NotImplementedError:
            print("Not implemented.")

        return False

    def lastModified(self):
        return os.stat(self.filepath).st_mtime


class OutputStream:

    def close(self):
        pass


class PrintWriter(OutputStream):

    def __init__(self, filepath, encoding=None):
        self.file = open(filepath, 'w')
        self.encode = encoding

    def println(self, line=""):
        self.file.writelines([line, "\n"])


class FileOutputStream(OutputStream):
    def __init__(self, filepath):
        self.file = open(filepath, 'w')


class InputStream:

    def close(self):
        pass


class FileInputStream(InputStream):

    def __init__(self, file):
        try:
            self.file = open(file.filepath, 'r')
        except Exception:
            raise IOException()

    def readLine(self):
        return self.file.readline().rstrip('\n')

    def readLines(self):
        return self.file.readlines()

    def read(self, size=1):
        return self.file.read(size)

    def close(self):
        self.file.close()
        pass


class FileReader(InputStream):

    def __init__(self, file):
        try:
            self.file = open(file.filepath, 'r')
        except Exception:
            raise IOException()

    def __enter__(self):
        return self.file

    def __exit__(self, type_, value, traceback):
        self.file.close()
        pass

    def readLine(self):
        return self.file.readline().rstrip('\n')

    def readLines(self):
        return self.file.readlines()

    def read(self, size=1):
        return self.file.read(size)

    def close(self):
        self.file.close()
        pass


class StringReader(InputStream):

    def __init__(self, text):
        self.stream = io.StringIO(text)

    def readLine(self):
        line = self.stream.readline()
        return None if not line else line.rstrip('\n')

    def readLines(self):
        return self.readLines()


class Properties:

    def __init__(self):
        self.props = {}

    def load(self, reader):
        config_string = '[dummy_section]\n' + reader.read()
        parser = ConfigParser()
        parser.read_string(config_string)
        self.props = parser['dummy_section']

    def getProperty(self, key):
        return self.props[key]


# noinspection PyMethodMayBeStatic
class Logger:

    def __init__(self, name):
        self.name = name

    @classmethod
    def getLogger(cls, name):
        return cls(name)

    def info(self, message):
        print(message)

    # noinspection PyMethodMayBeStatic
    def fine(self, message):
        if DEBUG:
            print(message)

    @classmethod
    def finer(cls, message):
        if DEBUG:
            print(message)


class Iterator:

    def __init__(self, iterable):
        self.iterator = iter(iterable)
        self.next_value = None
        self.closed = False

    def hasNext(self):
        if self.closed:
            return False
        if self.next_value is not None:
            return True

        try:
            self.next_value = self.iterator.__next__()
        except StopIteration:
            self.next_value = None

        if self.next_value is None:
            self.close()  # Auto-close on exit.
        return self.next_value is not None

    def next(self):
        if self.hasNext():
            value = self.next_value
            self.next_value = None
            return value
        else:
            raise NoSuchElementException()  # raises StopIteration

    def doClose(self):
        pass

    def close(self):
        if not self.closed:
            self.doClose()
            self.closed = True

    def isClosed(self):
        return self.closed

    def __next__(self):
        try:
            return self.next()
        except NoSuchElementException:
            raise StopIteration()


# class Iterable:
#     def iterator(self):
#         pass
#
#     def next(self):
#         pass


class Iterable:

    def __iter__(self):
        return self.iterator()

    def iterator(self):
        pass


class Set(set):

    def remove(self, element):
        try:
            super().remove(element)
            return True
        except KeyError:
            return False

    def isEmpty(self):
        return not bool(self)


class List(list, Iterable):

    def get(self, index):
        return self[index]

    def isEmpty(self):
        return not self

    def iterator(self):
        return Iterator(self)


class Stack(list):
    def isEmpty(self):
        return not self

    def push(self, item):
        self.append(item)

    def peek(self):
        return self[-1]


class TreeSet(OrderedDict):

    def add(self, key):
        self[key] = None
