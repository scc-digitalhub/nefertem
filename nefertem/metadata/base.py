"""
Metadata module.
"""

class Metadata:
    """
    Base class for metadata objects.
    """

    def to_dict(self) -> dict:
        """
        Render the object as a dictionary.

        Returns
        -------
        dict
            Dictionary representation of the object.
        """
        return self.__dict__

    def __repr__(self) -> str:
        return str(self.to_dict())
