from compat import Iterator, Iterable


class IWiktionaryIterator(Iterator, Iterable):
    """ A generic iterator that is used for Wiktionary data objects (i.e.,
        :@link IWiktionaryPage, :@link IWiktionaryEntry,
        :@link IWiktionarySense). The iterator supports both the usage as
        :@link Iterator and as :@link Iterable.
         *
        Caveat: the latter provides always the same instance, so use the
        WiktionaryIterator as an :@link Iterable only once or fetch another
        WiktionaryIterator for other uses. This should save some memory <i>and</i>
        allow convenient usage in numerous situations. Besides, the implementation
        also allows to react on stopping the iteration, which is the case if
        (a) all items have been traversed, or (b) the user manually stops the
        iteration by invoking the :@link #close() method. Implementing the
        corresponding hotspot offers the possibility of closing a connection
        or freeing a resource after iteration. The iterator is read-only.
        @param <IterableType> the object type that is the subject of iteration. """

    def close(self):
        """ Stops the iteration. This method is automatically called after all
            items are traversed, but needs to be called manually if the iteration
            is stopped before. Closing the iterator is necessary to guarantee
            data consistency and proper resource management. Closing an
            iterator multiple times has no effect. After an iterator is closed,
            :@link #hasNext() will always result in <code>False</code>. """
        pass

    def isClosed(self):
        """ Returns True if the iterator has been closed, which is the case
            after :@link #close() has been called or after the last element
            has been retrieved using the :@link #next() method. """
        pass
