""" ArboLib - storage: JSON file reader and writer

This module contains the JSON file reader and file writer.

copyright (C) 2016 Bram Rooseleer
"""

from .file_writer import FileWriterImpl

EXTENSION = "json"
"""The JSN default file extension."""


class JSONWriter(FileWriterImpl):
    """A JSON file writer."""

    def __init__(self, *args, **kwargs):
        self.indentation = 0
        super().__init__(*args, **kwargs)

    def write_reference(self, storable):
        """Write a reference to an already written Storable."""
        raise NotImplementedError()

    def write_single_field(self, name, value):
        """Write a single name-value pair to the file."""
        raise NotImplementedError()

    def write_list_field(self, name, list):
        """Write a single name-list/tuple pair to the file."""
        raise NotImplementedError()

    def write_dict_field(self, name, value):
        """Write a single name-dict pair to the file."""
        raise NotImplementedError()

    def open_file(self):
        self.file = open(self.path, 'w')

    def close_file(self):
        self.file.close()

    def write_header(self):
        pass

    def write_footer(self):
        pass

    def write_storable_start(self, storable):
        self.write_line('{')

    def write_storable_end(self, storable):
        self.write_line('}')

    def write(self, text):
        self.file.write(text)

    def write_line(self, text):
        self.write(text+'\n')

    @classmethod
    def extension(cls):
        return EXTENSION
