from nefertem.client.client import Client


def create_client(
    output_path: str | None = None,
    stores: list[dict] | None = None,
    tmp_dir: str | None = None,
) -> Client:
    """
    Create a new Client object.

    Parameters
    ----------
    output_path : str
        Path to the metadata store.
    stores : list[dict]
        List of dict containing configuration for the artifact stores.
    tmp_dir : str
        Default local temporary folder where to store input data".

    Returns
    -------
    Client
        Client object.
    """
    return Client(output_path, stores, tmp_dir)
