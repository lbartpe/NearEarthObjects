"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has
a unique primary designation, an optional unique name, an optional
diameter, and a flag for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an
NEO. Each has an approach datetime, a nominal approach distance, and
a relative approach velocity.

A `NearEarthObject` maintains a collection of its close approaches,
and a `CloseApproach` maintains a reference to its NEO.

The functions that construct these objects use information extracted
from the data files from NASA, so these objects should be able to
handle all of the quirks of the data set, such as missing names and
unknown diameters.
"""
from math import isnan

from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the
    object,such as its primary designation (required, unique), IAU
    name (optional), diameter in kilometers (optional - sometimes
    unknown), and whether it's marked as potentially hazardous to
    Earth.

    A `NearEarthObject` also maintains a collection of its close
    approaches - initialized to an empty collection, but eventually
    populated in the `NEODatabase` constructor.
    """

    def __init__(self, pdes, name, pha, diameter):
        """Create a new `NearEarthObject`.

        :param designation: The NEO’s primary designation.
        :param name: The NEO’s IAU name (could be empty, or None).
        :param diameter: The NEO’s diameter, in kilometers, or NaN.
        :param hazardous: Whether the NEO is potentially hazardous.
        :param approaches: A collection of this NEO’s
        CloseApproaches (initially an empty collection).
        """
        self.designation = str(pdes)
        self.name = str(name) or None

        def handle_hazard(pha):
            if pha == 'Y':
                return True
            else:
                return False

        self.hazardous = handle_hazard(pha)

        def validate_dia(diameter):
            if not diameter:
                raise Exception("Missing Diameter")
            return True

        try:
            if validate_dia(diameter):
                self.diameter = float(diameter)
        except:
            self.diameter = float('NaN')

        # Empty collection of this NEO's CloseApproach(es)
        self.approaches = []

    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        # Returns fullname from 'self.designation' and 'self.name' parameters
        # if they both exist.
        if self.name is not None:
            return f"{self.designation} {self.name}"
        else:
            return f"{self.designation}"

    @property
    def known_diameter(self):
        """Return a representation of the diameter if known."""
        # Returns diameter if known.
        is_nan = isnan(self.diameter)
        if is_nan is True:
            return f"an unknown diameter"
        else:
            return f"a diameter of {self.diameter:.3f} km"

    def __str__(self):
        """Return `str(self)`.

        A human--readable string representation of this object.
        """
        # Returns one of the following literal strings based on if the NEO is
        # hazardous or not.
        if self.hazardous is True:
            neo_string = (
                f"A Near Earth Object (NEO), {self.fullname}, has "
                f"{self.known_diameter} and is potentially hazardous.")
        else:
            neo_string = (
                f"A Near Earth Object (NEO), {self.fullname}, has "
                f"{self.known_diameter} and is not potentially hazardous.")
        return neo_string

    def __repr__(self):
        """Return `repr(self)`.

        A computer-readable string representation of this object.
        """
        return (
            f"NearEarthObject(designation={self.designation!r}, "
            f"name={self.name!r}, diameter={self.diameter:.3f}, "
            f"hazardous={self.hazardous!r})"
        )


class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close
    approach to Earth, such as the date and time (in UTC) of closest
    approach, the nominal approach distance in astronomical units, and
    the relative approach velocity in kilometers per second.

    A `CloseApproach` also maintains a reference to its
    `NearEarthObject` - initially, this information (the NEO's primary
    designation) is saved in a private attribute, but the referenced
    NEO is eventually replaced in the `NEODatabase` constructor.
    """

    def __init__(self, des, cd, dist, v_rel):
        """Create a new `CloseApproach`.

        :param cd:  The date and time, in UTC, at which the closest
        to Earth.
        :param dist: The nominal approach distance, in astronomical
        units, of the NEO to Earth at the closest point.
        :param v_rel: The velocity, in kilometers per second, of the
        NEO relative to Earth at the closest point.
        :param neo: A reference to the NearEarthObject that is making
        the close approach (initially None).
        :param des:  An additional attribute, to store the NEO’s
        primary designation before the CloseApproach is linked to its
        NearEarthObject.
        """
        self._designation = str(des)
        self.time = cd_to_datetime(cd)
        self.distance = float(dist)
        self.velocity = float(v_rel)

        # Initial value for the NEO who made the close approach:
        def validate_des(des):
            if not des:
                raise Exception("Missing Designation")
            return True

        try:
            if validate_des(des):
                self.neo = str(des)
        except:
            self.neo = None

    def link_neo(self, neos):
        """Return linked NEOs.

        A function to link individual NEOs to the corresponding
        CloseApproach's '.neo' attribute, and subsequently append
        the closeApproach to the '.approaches' attribute previously
        left as an empty list.

        :param neos: Dictionary comprehension to return neo with a
        matching '.designation' to the approach '._designation'.
        :return: The linked neo and subsequently linked approach for
        use in the 'database.py' module.
        """
        if self._designation in neos:
            # Sets linked NearEarthObject to CloseApproach's '.neo' attribute.
            self.neo = neos[self._designation]
            # Subsequently appends CloseApproach to linked NearEarthObject's
            # '.approaches' attribute.
            self.neo.approaches.append(self)
        else:
            self.neo = None
        return self

    @property
    def time_str(self):
        """Return this `CloseApproach`'s approach time.

        The value in `self.time` should be a Python `datetime` object.
        While a `datetime` object has a string representation, the
        default representation includes seconds - significant figures
        that don't exist in our input data set.

        The `datetime_to_str` method converts a `datetime` object to
        a formatted string that can be used in human-readable
        representations and in serialization to CSV and JSON files.
        """
        return datetime_to_str(self.time)

    def __str__(self):
        """Return `str(self)`.

        A human--readable string representation of this object.
        """
        ca_string = (
                f"At {self.time_str}, {self._designation} approaches "
                f"Earth at a distance of {self.distance:.2f} au and a "
                f"velocity of {self.velocity:.2f} km/s.")
        return ca_string

    def __repr__(self):
        """Return `repr(self)'.'

        A computer-readable string representation of this object.
        """
        return (f"CloseApproach(time={self.time_str!r}, "
                f"distance={self.distance:.2f}, "
                f"velocity={self.velocity:.2f}, "
                f"neo={self.neo!r})"
                )

    def serialize(self, extension):
        """Serialize CVS and JSON data.

        :param extension: Out file extension.  It must be '.csv' or
        '.json' and should throw a ValueError if not.
        :return: A serialized dictionary to be used to 'write_to_csv'
        and 'write_to_json' in the 'write.py' module.
        """
        # Serialize CSV:
        if extension == 'csv':
            serialized_dict = {'datetime_utc': self.time_str,
                               'distance_au': self.distance,
                               'velocity_km_s': self.velocity,
                               'designation': self.neo.designation,
                               'name': self.neo.name,
                               'diameter_km': self.neo.diameter,
                               'potentially_hazardous': self.neo.hazardous
                               }
            return serialized_dict

        # Serialize JSON:
        if extension == 'json':
            serialized_dict = {'datetime_utc': self.time_str,
                               'distance_au': self.distance,
                               'velocity_km_s': self.velocity,
                               'neo': {'designation': self.neo.designation,
                                       'name': self.neo.name,
                                       'diameter_km': self.neo.diameter,
                                       'potentially_hazardous':
                                       self.neo.hazardous
                                       }
                               }
            return serialized_dict

        # Raise ValueError if file extension is invalid:
        if extension not in ('csv', 'json'):
            raise ValueError(f"Invalid file extension: '{extension!r}'. \n"
                             f"Please specify one of the valid extensions: "
                             f"'csv' or 'json' \n\n"
                             )


if __name__ == '__main__':
    print(f"First Module's Name: {__name__}\n")
