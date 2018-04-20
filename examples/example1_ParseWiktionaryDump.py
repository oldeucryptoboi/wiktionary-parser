import os

from PyWKTL import PyWKTL

from api import WiktionaryFormatter
from compat import File
from errors import IllegalArgumentException


class Example1ParseWiktionaryDump:
    """ Simple example for parsing a Wiktionary dump file and printing the
        entries for the word <i>Wiktionary</i>. """

    @staticmethod
    def main():

        import sys

        args = sys.argv[1:]
        for arg in args:
            print(arg)

        """ Runs the example.
            @param args name of the dump file, output directory for parsed data,
                boolean value that specifies if existing parsed data should
            be deleted. """

        if len(args) != 3:
            raise IllegalArgumentException("Too few arguments. "
                                           + "Required arguments: <DUMP_FILE> <OUTPUT_DIRECTORY> "
                                           + "<OVERWRITE_EXISTING_DATA>")

        dumpFile = File(os.path.dirname(args[0]), os.path.basename(args[0]))
        outputDirectory = File(args[1], "")
        overwriteExisting = bool(args[2])

        # Parse dump file
        PyWKTL.parseWiktionaryDump(dumpFile, outputDirectory, overwriteExisting)

        # Create IWiktionaryEdition for our parsed data.
        wkt = PyWKTL.openEdition(outputDirectory)

        # Retrieve all IWiktionaryEntries for the word "Wiktionary".
        entries = wkt.getEntriesForWord("Wiktionary")

        # Print the information of the parsed entries.
        for entry in entries:
            print(WiktionaryFormatter.formatHeaderForEntry(entry))

        # Close the Wiktionary edition.
        wkt.close()


if __name__ == '__main__':
    Example1ParseWiktionaryDump.main()
    # Example1ParseWiktionaryDump.main()
