class EokulDictable:
    """EokulDictable model
    Provides a method to convert a dict to object and another method to create object with empty values
    """

    @classmethod
    def from_dict(cls, obj: dict):
        """Converts a dict to object

        Args:
            obj (dict): Object to be converted

        Returns:
            object: Object that is converted from dict
        """
        return cls(**obj)

    @classmethod
    def empty(cls):
        """Creates an object with empty values

        Returns:
            object: Object with empty values
        """
        return cls()
