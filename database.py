"""Encapsulating database.

A database encapsulating collections of near-Earth objects and
their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close
approaches.  It provides methods to fetch an NEO by primary
designation or by name, as well as a method to query the set of
close approaches that match a collection of user-specified criteria.

Under normal circumstances, the main module creates one NEODatabase
from the data on NEOs and close approaches extracted by
`extract.load_neos` and `extract.load_approaches`.
"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of
    close approaches. It additionally maintains a few auxiliary data
    structures to help fetch NEOs by primary designation or by name
    and to help speed up querying for close approaches that match
    criteria.
    """

    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the
        collections of NEOs and close approaches haven't yet been
        linked - that is, the `.approaches` attribute of each
        `NearEarthObject` resolves to an empty collection, and the
        `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute
        (`._designation`) that matches the `.designation` attribute of
        the corresponding NEO. This constructor modifies the supplied
        NEOs and close approaches to link them together - after it's
        done, the `.approaches` attribute of each NEO has a collection
        of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neo_by_name: A dictionary comprehension of NEOs with
        the key value being the name of the NEO.
        :param neo_by_designation: A dictionary comprehension of NEOs
        with the key value being the primary designation of the NEO.
        :param approaches: A collection of `CloseApproach`es  with
        corresponding neos populated and subsequently populated approaches.
        :param neos: A collection of `NearEarthObject`s with
        corresponding approaches populated.
        """
        # Dictionary comprehension to find neo by '.name':
        self.neo_by_name = {i.name: i for i in neos}
        # Dictionary comprehension to find neo by '.designation':
        self.neo_by_designation = {i.designation: i for i in neos}

        # List comprehension of approaches with linked neos and subsequently
        # linked approaches to 'linked_neo'.
        self._approaches = [i.link_neo(self.neo_by_designation)
                            for i in approaches]

        # List comprehension of neos with linked approaches from above linked
        # 'self_approaches'.  This parameter is not used as lookup for querying
        # or any other function or method moving forward in program, but it
        # could be with minor coding changes, if determined necessary in the
        # future.
        self._neos = [i.neo for i in self._approaches]

    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as
        a string.

        The matching is exact - check for spelling and capitalization
        if no match is found.

        :param designation: The primary designation of the NEO to
        search for.
        :return: The `NearEarthObject` with the desired primary
        designation, or `None`.
        """
        if designation in self.neo_by_designation:
            return self.neo_by_designation.get(designation)
        else:
            return None

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are
        associated with the empty string nor with the `None`
        singleton.

        The matching is exact - check for spelling and
        capitalization if no match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or
        `None`.
        """
        if name in self.neo_by_name:
            return self.neo_by_name.get(name)
        else:
            return None

    def query(self, filters=()):
        """Return filtered or unfiltered approaches.

        Query close approaches to generate those that match a
        collection of filters.

        This generates a stream of `CloseApproach` objects that match
        all of the provided filters.

        If no arguments are provided, generate all known close
        approaches.

        The `CloseApproach` objects are generated in internal order,
        which isn't guaranteed to be sorted meaningfully, although is
        often sorted by time.

        :param filters: A collection of filters capturing
        user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
        # All known close approaches:
        approaches = self._approaches
        # All known, filtered approaches (if filters exist):
        if filters:
            for _filter in filters:
                approaches = filter(_filter, approaches)
        # Generates filtered or unfiltered approaches depending on
        # if filters exist or not:
        for approach in approaches:
            yield approach


if __name__ == '__main__':
    print(f"\nFirst Module's Name: {__name__}\n\n")
