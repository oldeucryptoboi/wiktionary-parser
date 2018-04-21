from enum import Enum


class Environment:
    def __init__(self, path, config):
        self.path = path
        self.config = config

    def getConfig(self):
        return self.config

    def sync(self):
        pass

    def close(self):
        pass


class EnvironmentConfig:

    allowCreateNew = False
    isReadOnly = False
    state = False
    cacheSize = False


    def setAllowCreate(self, allowCreateNew):
        self.allowCreateNew = allowCreateNew
        pass

    def setReadOnly(self, isReadOnly):
        self.isReadOnly = isReadOnly
        pass

    def setTransactional(self, state):
        self.state = state
        pass

    def setCacheSize(self, cacheSize):
        self.cacheSize = cacheSize
        pass

    def getReadOnly(self):
        return self.isReadOnly

    def getCacheSize(self):
        return self.cacheSize


class BasicIndex:
    pass


class PrimaryIndex(BasicIndex):
    def gef(self):
        pass

    def put(self, entity):
        print("storing " + str(entity))
        return None


class SecondaryIndex(BasicIndex):
    def gef(self):
        pass


class StoreConfig:
    def setAllowCreate(self, allowCreateNew):
        pass

    def setTransactional(self, state):
        pass

    def setReadOnly(self, isReadOnly):
        pass


# noinspection PyUnusedLocal
class EntityStore:

    def __init__(self, env, dbname, store_config):
        pass

    # noinspection PyMethodMayBeStatic
    def getPrimaryIndex(self, cls1, cls2):
        return PrimaryIndex()

    # noinspection PyMethodMayBeStatic
    def getSecondaryIndex(self, id_, cls, name):
        return SecondaryIndex()

    def close(self):
        pass


class CursorConfig(Enum):

    DEFAULT = 1
