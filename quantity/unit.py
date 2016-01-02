"""

"""
from functools import total_ordering


@total_ordering
class Unit:
    """A class representing units."""

    _existing_units = []
    """A list containing the existing units with a symbol."""

    @staticmethod
    def _get_unit_for(unit_powers, scale):
        """Private method to generate or retrieve the needed unit."""
        result = Unit(name=None, symbol=None, unit_powers=unit_powers, scale=scale)
        if result in Unit._existing_units:
            return Unit._existing_units[Unit._existing_units.index(result)]
        else:
            return result

    def __init__(self, name, symbol, unit_powers=None, scale=1.0):
        """ Create a unit.

        A unit is defined in function of powers of base units and a scale factor. These are given in a dictionary
        'unit_powers' mapping base units on the power they have in this unit and the number 'scale'. If 'unit_powers' is
        not given, the unit is considered to be a base unit. I then cannot have a scale.

        In additional a unit can have a name and/or a symbol. A unit with a symbol will be entered in an internal lookup
        list, so the symbol (and name) can be reused when a similar unit is made.
        """
        self._name = name
        self._symbol = symbol
        if unit_powers is not None:
            self._unit_powers = {unit: power for unit, power in unit_powers.items() if power != 0}
            units = tuple(sorted(unit_powers.keys()))
            powers = (unit_powers[unit] for unit in units)
            self._hash = hash((units, powers))
        else:
            self._hash = hash(symbol)
            self._unit_powers = {self: 1}
            if scale != 1.0:
                raise TypeError("A base unit cannot have a scale that is not 1")
        self._scale = scale

        if symbol is not None:
            Unit._existing_units.append(self)

    @property
    def name(self):
        """Return the name of the unit."""
        return self._name

    @property
    def symbol(self):
        """Return the name of the unit."""
        return self._symbol

    @property
    def unit_powers(self):
        """Return a dict which maps the basic SI units on its power in this unit."""
        return self._unit_powers.copy()

    @property
    def scale(self):
        """Return the scale of this unit."""
        return self._scale

    def __eq__(self, other):
        """Return whether the given unit is equal to this one."""
        for unit in self.unit_powers:
            if unit in other.unit_powers:
                if self.unit_powers[unit] != other.unit_powers[unit]:
                    return False
            elif self.unit_powers[unit] != 0:
                return False
        for unit in other.unit_powers:
            if unit in self.unit_powers:
                if self.unit_powers[unit] != other.unit_powers[unit]:
                    return False
            elif other.unit_powers[unit] != 0:
                return False
        return True

    def __ne__(self, other):
        """Return whether the given unit is unequal to this one."""
        return not self == other

    def __str__(self):
        """Return a string representation of this unit."""
        if self.symbol is not None:
            return self.symbol
        else:
            if self.scale != 1:
                result = str(self.scale)
            else:
                result = ''
            for unit in sorted(self.unit_powers.keys()):
                power = self.unit_powers[unit]
                if power != 0:
                    result += str(unit)
                if power != 1:
                    result += str(power)
            return result

    def __mul__(self, other):
        """Multiply this unit with the given unit. Return a compatible existing unit if possible."""
        unit_powers = self.unit_powers
        for unit in other.unit_powers:
            if unit in unit_powers:
                unit_powers[unit] += other.unit_powers[unit]
            else:
                unit_powers[unit] = other.unit_powers[unit]
        scale = self.scale*other.scale
        return Unit._get_unit_for(unit_powers=unit_powers, scale=scale)

    def __pow__(self, other):
        """Raises this unit to an (integer) power."""
        if not other == int(other):
            raise TypeError("only integer powers of units are allowed.")
        result = ONE
        for i in range(abs(int(other))):
            if other < 0:
                result = result/self
            else:
                result = result*self
        return result

    def __truediv__(self, other):
        """Divide this unit by the given unit. Return a compatible existing unit if possible."""
        unit_powers = self.unit_powers
        for unit in other.unit_powers:
            if unit in unit_powers:
                unit_powers[unit] -= other.unit_powers[unit]
            else:
                unit_powers[unit] = -other.unit_powers[unit]
        scale = self.scale/other.scale
        return Unit._get_unit_for(unit_powers=unit_powers, scale=scale)

    def __hash__(self):
        """Return the hash of this unit."""
        return self._hash

    def __lt__(self, other):
        """Compare the units for sorting, this is done alphabetically using the symbol."""
        return self.symbol < other.symbol

    def with_name_symbol(self, name=None, symbol=None):
        """Adds name and/or symbol to the unit."""
        return Unit(name=name, symbol=symbol, unit_powers=self.unit_powers, scale=self.scale)

# Dimensionless unit

ONE = Unit(name='one', symbol='',  unit_powers={})

# SI base units

METRE = Unit(name='metre', symbol='m')
"""The SI base unit of length"""

KILOGRAM = Unit(name='kilogram', symbol='kg')
"""The SI base unit of mass"""

SECOND = Unit(name='second', symbol='s')
"""The SI base unit of time"""

AMPERE = Unit(name='ampere', symbol='A')
"""The SI base unit of current"""

KELVIN = Unit(name='kelvin', symbol='K')
"""The SI base unit of temperature"""

CANDELA = Unit(name='candela', symbol='cd')
"""The SI base unit of length"""

MOLE = Unit(name='mole', symbol='mol')
"""The SI base unit of amount of substance"""

# SI additional geometrical units

METRE2 = METRE**2
"""The SI unit of area"""

METRE3 = METRE**3
"""The SI unit of volume"""

# SI additional mechanical units

MPS = METRE/SECOND
"""The SI unit of speed"""

MPS2 = METRE/(SECOND**2)
"""The SI unit of acceleration"""

NEWTON = (KILOGRAM*MPS2).with_name_symbol(name='newton', symbol='N')
"""The SI unit of force"""

PASCAL = (NEWTON/METRE2).with_name_symbol(name='pascal', symbol='Pa')
"""The SI unit of pressure"""

JOULE = (NEWTON*METRE).with_name_symbol(name='joule', symbol='J')
"""The SI unit of energy"""

WATT = (JOULE/SECOND).with_name_symbol(name='watt', symbol='W')
"""The SI unit of energy"""

# SI additional electrical units

COULOMB = (AMPERE*SECOND).with_name_symbol(name='coulomb', symbol='C')
"""The SI unit of charge."""

VOLT = (JOULE/COULOMB).with_name_symbol(name='volt', symbol='V')
"""The SI unit of electrical potential."""

OHM = (VOLT/AMPERE).with_name_symbol(name='ohm', symbol='Ohm')
"""The SI unit of electrical resistance."""

FARAD = (COULOMB/VOLT).with_name_symbol(name='farad', symbol='F')
"""The SI unit of electrical resistance."""

HENRI = (VOLT/(AMPERE/SECOND)).with_name_symbol(name='henri', symbol='H')
"""The SI unit of electrical resistance."""
