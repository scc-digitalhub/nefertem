"""
Nefertem Inference Plugin Utils.
"""


def get_fields(name: str = None, type_: str = None) -> dict:
    """
    Return a common field structure.

    Parameters
    ----------
    name : str
        Field name.
    type_ : str
        Field type.

    Returns
    -------
    dict
        Field structure.
    """
    return {"name": name, "type": type_}
