"""
Utils functions for data reader.
"""
from frictionless import Detector, Resource


def describe_resource(pth: str) -> dict:
    """
    Describe a resource using frictionless.

    With bigger buffer/sample we should avoid error encoding detection.

    Parameters
    ----------
    pth: str
        Path to resource.

    Returns
    -------
    dict
        Resource description.
    """
    return Resource.describe(source=pth, detector=Detector(buffer_size=20000, sample_size=1250)).to_dict()
