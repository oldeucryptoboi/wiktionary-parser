from enum import Enum


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
