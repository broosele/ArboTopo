""" ArboLib - storage: file writer

The FileWriter class of this module is an abstract implementation of a class used to write a Storable to a file.

copyright (C) 2016 Bram Rooseleer
"""

from .storable import Storable


class FileWriter:
    """An abstract file writer."""

    def __init__(self, path, *storables):
        """Create a file writer."""
        self.path = path
        self.storables = list(storables)

    # def add_storable(self, *storables):
    #     """Add a Storable to the list of Storables to be written."""
    #     for storable in storables:
    #         self.storables.append(storable)

    def write_to_file(self):
        """Write the content to the file."""
        raise NotImplementedError()


class FileWriterImpl(FileWriter):
    """An partial implementation of a FileWriter."""

    def write_to_file(self):
        already_written = set()
        with self:
            self.write_header()
            for storable in self.storables:
                self.write_storable(storable, already_written)
            self.write_footer()
        self.close_file()

    def write_storable(self, storable, already_written):
        """Write a storable to the file.

        This includes the storables referenced by the storable to be written. No Storable is written twice.
        """
        if self in already_written:
            self.write_reference(storable)
        else:
            already_written.add(self)
            self.write_storable_start(storable)
            content = storable.serialize()
            for name, value in content.item():
                if isinstance(value, (int, float, str)):
                    self.write_single_field(name, value)
                elif isinstance(value, (list, tuple)):
                    self.write_list_field(name, value)
                elif isinstance(value, dict):
                    self.write_dict_field(name, value)
                elif isinstance(value, Storable):
                    self.write_storable(value, already_written)
                else:
                    TypeError("Field of type '{type}' cannot be stored.".format(type=type(value).__name__))
            self.write_storable_end(storable)

    def __enter__(self):
        self.open_file()

    def __exit__(self):
        self.close_file()

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
        """Open the file."""
        raise NotImplementedError()

    def close_file(self):
        """Close the file."""
        raise NotImplementedError()

    def write_header(self):
        """Write the header."""
        raise NotImplementedError()

    def write_footer(self):
        """Write the footer."""
        raise NotImplementedError()

    def write_storable_start(self, storable):
        """Write the start of a storable."""
        raise NotImplementedError()

    def write_storable_end(self, storable):
        """Write the end or a storable."""
        raise NotImplementedError()

    @classmethod
    def extension(cls):
        """Return the extension for this type of file."""
        raise NotImplementedError()
