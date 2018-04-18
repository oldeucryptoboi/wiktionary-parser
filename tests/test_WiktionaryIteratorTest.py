import unittest
import collections

from api.util import WiktionaryIterator
from errors import NoSuchElementException, UnsupportedOperationException


class TestWiktionaryIterator(unittest.TestCase):

    queue = collections.deque()

    class MyWiktionaryIterator(WiktionaryIterator):

        def __init__(self, outer):
            super().__init__()
            self.outer = outer

        def doClose(self):
            if self.outer.wasClosed:
                self.outer.fail("Iteration was closed twice!")
            self.outer.wasClosed = True

        def fetchNext(self):
            if not self.outer.queue:
                return None

            try:
                elem = self.outer.queue.popleft()
            except StopIteration:
                elem = None
            return elem
            # return None if self.outer.queue.isEmpty() else self.outer.queue.get()

    def testSimpleIterator(self):

        # Normal iteration, 2 elements.
        self.queue.clear()
        self.wasClosed = False

        self.queue.append("test1")
        self.queue.append("test2")
        iter1 = self.MyWiktionaryIterator(self)
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("test1", iter1.next())
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("test2", iter1.next())
        self.assertFalse(iter1.hasNext())
        self.assertTrue(iter1.isClosed())
        self.assertTrue(not self.queue)
        self.assertTrue(self.wasClosed)

        # Normal iteration, 1 element.
        self.queue.clear()
        self.wasClosed = False
        
        self.queue.append("")
        iter1 = self.MyWiktionaryIterator(self)
        
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("", iter1.next())
        self.assertFalse(iter1.hasNext())
        self.assertTrue(iter1.isClosed())
        self.assertTrue(not self.queue)
        self.assertTrue(self.wasClosed)

        # Normal iteration, 0 elements.
        self.queue.clear()
        self.wasClosed = False
        iter1 = self.MyWiktionaryIterator(self)
        self.assertFalse(iter1.hasNext())
        self.assertTrue(iter1.isClosed())
        self.assertTrue(not self.queue)
        self.assertTrue(self.wasClosed)

        # Manual termination.
        self.queue.clear()
        self.wasClosed = False
        self.queue.append("test1")
        self.queue.append("test2")
        self.queue.append("test3")
        iter1 = self.MyWiktionaryIterator(self)
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("test1", iter1.next())
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertFalse(not self.queue)
        self.assertFalse(self.wasClosed)
        iter1.close()
        self.assertFalse(iter1.hasNext())
        self.assertTrue(iter1.isClosed())
        self.assertFalse(not self.queue)
        self.assertTrue(self.wasClosed)
        try:
            iter1.next()
            self.fail("NoSuchElementException expected")
        except NoSuchElementException:
            pass
    
        # Multiple terminations.
        wasClosed = False
        iter1.close()
        self.assertFalse(iter1.hasNext())
        self.assertTrue(iter1.isClosed())
        self.assertFalse(not self.queue)
        self.assertFalse(wasClosed)  # the close() method should not be called twice!
        try:
            iter1.next()
            self.fail("NoSuchElementException expected")
        except NoSuchElementException:
            pass
    
        # No multiple iterations.
        self.queue.clear()
        self.wasClosed = False
        self.queue.append("test1")
        self.queue.append("test2")
        self.queue.append("test3")
        self.queue.append("test4")
        iter1 = self.MyWiktionaryIterator(self)
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("test1", iter1.next())
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        iter2 = iter1.iterator()
        self.assertTrue(iter2.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("test2", iter2.next())
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("test3", iter1.next())
        self.assertTrue(iter2.hasNext())
        self.assertFalse(iter1.isClosed())
        self.assertEqual("test4", iter2.next())
        self.assertFalse(iter1.hasNext())
        self.assertTrue(iter1.isClosed())
        self.assertFalse(iter2.hasNext())
        self.assertTrue(not self.queue)
        self.assertTrue(self.wasClosed)
    
        # Read only.
        self.queue.clear()
        self.wasClosed = False
        self.queue.append("test")
        iter1 = self.MyWiktionaryIterator(self)
        self.assertTrue(iter1.hasNext())
        self.assertFalse(iter1.isClosed())
        try:
            iter1.remove()
            self.fail("UnsupportedOperationException expected")
        except UnsupportedOperationException:
            pass
        iter1.close()


if __name__ == '__main__':
    unittest.main()
