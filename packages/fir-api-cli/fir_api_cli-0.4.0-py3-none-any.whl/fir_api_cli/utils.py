import csv
from pathlib import Path
from time import gmtime, strftime
from typing import Dict, List

import requests
from tqdm import tqdm


def save_to_csv(data: List[Dict],
                filepath: Path,
                encoding: str = 'UTF8',
                newline: str = '',
                max_file_size: int = 2*1024**3) -> None:  # 2GB
    """Save data to csv."""

    if not filepath.is_file():
        with open(filepath, 'w', encoding=encoding, newline=newline) as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
    else:
        file_size = filepath.stat().st_size
        if file_size > max_file_size:
            filepath = filepath.parent / (
                filepath.stem + '_' +
                strftime("%Y-%m-%dT%H%M%S", gmtime()) + filepath.suffix)
            with open(filepath, 'w', encoding=encoding, newline=newline) as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
        else:
            with open(filepath, 'a', encoding=encoding, newline=newline) as file:
                writer = csv.DictWriter(file, fieldnames=data[0].keys())
                writer.writerows(data)


def get_response(url: str, headers: Dict = None,
                 stream: bool = True, timeout: int = 60) -> requests.Response:
    """Get requests response from url."""
    if not headers:
        headers = {}
    try:
        response = requests.get(url, headers=headers,
                                stream=stream, timeout=timeout)
        return response
    except Exception as exc:
        raise exc


def download_from_url(url: str, headers: Dict,
                      path_to_save: Path, size: int) -> None:
    """Download data from url."""

    response = get_response(url, headers)
    progress_bar = tqdm(total=size, desc="Downloading", unit="B",
                        unit_scale=True, unit_divisor=1024, colour='#f6ff00')

    with open(path_to_save, "wb") as file:
        total_size = 0
        for data in response.iter_content(chunk_size=4096):
            total_size = total_size + len(data)
            # Write the data to the file
            file.write(data)
            # Update the progress progress_bar
            progress_bar.update(len(data))
        if total_size < size:
            progress_bar.update(size - total_size + 1)

    progress_bar.close()
