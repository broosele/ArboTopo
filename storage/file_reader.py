""" ArboLib - storage: file_reader

This class represents a reader for a file used to store Storables.

copyright (C) 2016 Bram Rooseleer
"""


class FileReader:
    """An abstract file reader."""

    @classmethod
    def get_extensions(cls):
        """Return the supported file extensions."""
        raise NotImplementedError()

    def __init__(self, path):
        """Create a read wrapper around a file."""
        self.path = path

    def get_content(self):
        """Read the file and return a dict of datasets."""
        self.add_file(datasets={})

    def add_contentself, datasets, join='illegal'):
        """Add the content of the file to the dict of datasets.

        The join argument determines what should be done when datasets are encountered with a name that already exist:
        -'illegal':     an exception will be raised
        -'add':         non-existing measurements, devices or properties will be added, an exception will be raised if
                        an item already exists
        -'replace':     the new dataset will fully replace the old one
        -'overwrite':   the new measurements, devices or properties will be added and will overwrite old data
        """
        self._open_file()
        extra_datasets = self._parse_file()

        self._close_file()

    def _open_file(self):
        """Open the file (abstract).

        Execute the code to be run before content can be read.
        """
        raise NotImplementedError()

    def _close_file(self):
        """Close the file (abstract).

        Execute the code to needed to end the file reading.
        """
        raise NotImplementedError()

    def _parse_file(self):
        """Parse the content of the file."""


