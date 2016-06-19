""" ArboLib - storage: storable

The Storable class represents an object which can be stored in a file. To be storable, a class should inherit from the
abstract class 'Storable' and implement the needed functions. This module also contains StorableImpl class implementing
part of the needed functionality and a function 'recreate_storable' which is a factory method to (re)create Storables.

Serialization:
 The 'serialize(self)' function should return a tuple with the type name, id (unique identifier) and content (dict with
 the fields to be stored. The fields in content can be lists, tuples, dicts, strings, booleans, numerical values or
 other Storables. Hierarchies of the allowed containers are also possible.

Deserialization:
 A storable is deserialized by using the id and content given at serialization as keyword arguments to the constructor.
 The keyword-value pair 'deserialize=True' is added to differentiate from normal instantiation. References to Storable
 objects are replaced by their id. When the referenced Storable has been created, the function
 'link_storable(self, id, storable)' is called. When the all objects have been recreated, the function
 'deserialize(self)' is called.

Limitations:
-the class name of the Storable needs to be unique as it is used to identify the type
-no objects other than Storables and the mentioned build-in types are allowed
-ids need to be unique
-fields cannot be named 'id', 'type' or 'deserialize'

copyright (C) 2016 Bram Rooseleer
"""


class Storable:
    """An abstract parent class for classes which can be stored in a file and loaded from a file."""

    def deserialize(self):
        """Finish the deserialization of this Storable object.

        This function is called at when all stored object have been recreated and linked. It is called on all Recreated
        objects in a random order.
        """
        raise NotImplementedError()

    def link_storable(self, id, storable):
        """Recreate the link with the newly recreated Storable.

        This function is called at when a Storable object which was referenced by this Storable object has been
        recreated. At this point the reference to the object should be made.
        """
        raise NotImplementedError()

    def serialize(self):
        """Return the content of this Storable object.

        The return value is a tuple with the following values:
        -type name
        -id (unique identifier)
        -content (dict with all fields that need to be stored)
        """
        raise NotImplementedError()

    @classmethod
    def type_name(cls):
        """Return a (unique) type name."""
        raise NotImplementedError()


class StorableImpl(Storable):
    """A class implementing some features of a Storable."""

    def __init__(self, deserialize=False, id=None, **kwargs):
        """Create a Storable item."""
        if deserialize:
            self.id = id
            self.deserialize_fields(**kwargs)
        else:
            self._init(id=id, **kwargs)

    def _init(self, **kwargs):
        """To be overwritten as initializer."""

    def deserialize_fields(self, **kwargs):
        """Recreate this Storable with the given fields."""
        raise NotImplementedError()

    def deserialize(self):
        pass

    def link_storable(self, storable):
        pass

    def serialize(self):
        return self.type_name(), self.id, self.content()

    def content(self):
        """Return the fields defining the content of this Storable."""
        raise NotImplementedError()

    @classmethod
    def type_name(cls):
        return cls.__module__ + '.' + cls.__name__


def recreate_storable(type, id, content):
    """Recreate a Storable with type as class id."""
    for cls in Storable.__subclasses__():
        if cls.type_name() == type:
            return cls(id=id, **content)
