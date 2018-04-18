from .IWiktionaryIterator import IWiktionaryIterator
from errors import NoSuchElementException, UnsupportedOperationException


class WiktionaryIterator(IWiktionaryIterator):
    """   Default implementation of the :@link IWiktionaryIterator interface. """

    def __init__(self):
        self.nextValue = None
        self.closed = False

    def iterator(self):
        return self

    def hasNext(self):
        if self.closed:
            return False
        if self.nextValue is not None:
            return True

        self.nextValue = self.fetchNext()
        if self.nextValue is None:
            self.close()  # Auto-close on exit.
        return self.nextValue is not None

    def next(self):
        if self.hasNext():
            value = self.nextValue
            self.nextValue = None
            return value
        else:
            raise NoSuchElementException()  # raises StopIteration

    def fetchNext(self):
        """ Hotspot for fetching the next element for iteration. If there are no
            elements left, <code>None</code> is to be returned, which causes the
            iterator to return <code>False</code> for the next :@link #hasNext(). """
        return None

    def doClose(self):
        """ Hotspot that is invoked after closing the iteration, i.e. either all
            items are traversed or manual termination. The hotspot is called only
            once. """
        pass

    def remove(self):
        raise UnsupportedOperationException("PyWKTL access is read-only.")

    def close(self):
        if not self.closed:
            self.doClose()
            self.closed = True

    def isClosed(self):
        return self.closed
