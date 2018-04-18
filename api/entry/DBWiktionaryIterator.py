from errors import WiktionaryException, DatabaseException
from api.util import WiktionaryIterator


# noinspection PyMethodMayBeStatic
class DBWiktionaryIterator(WiktionaryIterator):
    """ Implementation of the :@link WiktionaryIterator for the use of a
        DataBase :@link EntityCursor as a source of elements. The cursor
        is passed to the constructor and automatically closed upon manually
        termination of the iteration or after all elements have been traversed.
        Additionally, a hotspot is provided to react on the return of an
        element of the cursor to, e.g., initialize the entity. It is
        possible to convert the stored entity to a more general type
        using different type parameters.
        @param <OutputType> the class type that is returned for each
            fetched element.
        @param <InputType> the class type the stored entities have. It
            is necessary that the input type is the same or a subclass
            of the type specified as output. """

    def __init__(self, edition, cursor):
        """ Initializes the iterator for the specified cursor. """
        self.edition = edition
        self.cursor = cursor
        self.edition.openCursors.add(cursor)

    def fetchNext(self):
        try:
            if self.closed:
                return None

            while True:
                next_cursor = self.cursor.next()
                if next_cursor is None:
                    return None

                result = self.loadEntity(next_cursor)
                if result is not None:
                    return result

            # return loadEntity(cursor.next())
        except DatabaseException as e:
            raise WiktionaryException(e)

    def loadEntity(self, entity):
        """ Hotspot that is invoked when returning an entity. It can, e.g.,
            be used to initialize the entity before usage. """
        return entity

    def doClose(self):
        try:
            self.cursor.close()
            self.edition.openCursors.remove(self.cursor)
        except DatabaseException as e:
            raise WiktionaryException(e)
