import functools
import pathlib
import shutil
import zipfile
from typing import Union

import requests
from tqdm import tqdm


def download_data(file_name: str, link: str, extract_dir: Union[pathlib.Path, str] = None):
    """
    Download a zipfile from the specified link and extract it to a directory.
    """
    r = requests.get(link, stream=True, allow_redirects=True)
    if r.status_code != 200:
        r.raise_for_status()  # Will only raise for 4xx codes, so...
        raise RuntimeError(f"Request to {link} returned status code {r.status_code}")
    file_size = int(r.headers.get("Content-Length", 0))

    path = pathlib.Path(file_name).expanduser().resolve()
    path.parent.mkdir(parents=True, exist_ok=True)

    desc = "(Unknown total file size)" if file_size == 0 else ""
    r.raw.read = functools.partial(
        r.raw.read, decode_content=True
    )  # Decompress if needed
    with tqdm.wrapattr(r.raw, "read", total=file_size, desc=desc) as r_raw:
        with path.open("wb") as f:
            shutil.copyfileobj(r_raw, f)

    # Unzip downloaded file (default to current directory)
    if extract_dir is None:
        extract_dir = pathlib.Path(".")
    with zipfile.ZipFile(file_name, "r") as zip_ref:
        zip_ref.extractall(extract_dir)
