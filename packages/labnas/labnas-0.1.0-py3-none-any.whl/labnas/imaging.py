"""NAS interactions specific to imaging data."""

import os
from pathlib import Path

import pandas as pd
from tqdm import tqdm

from labnas.base import SftpConnection
from labnas.local import convert_tif_folder_into_file


class ImagingConnection(SftpConnection):
    def scan(self, remote_folder: Path) -> pd.DataFrame:
        rows = []

        files, subject_folders = self.list_files_and_folder(remote_folder)
        for subject_folder in subject_folders:
            sessions_folder = subject_folder / "sessions"
            if self.connection.isdir(str(sessions_folder)):
                files, date_folders = self.list_files_and_folder(subject_folder / "sessions")
                for date_folder in date_folders:
                    files, dtype_folders = self.list_files_and_folder(date_folder)
                    for dtype_folder in dtype_folders:
                        details = {
                            "subject_id": subject_folder.name,
                            "date": date_folder.name,
                            "dtype": dtype_folder.name,
                        }
                        rows.append(details)
        rows = pd.DataFrame(rows)
        return rows

    def download_as_single_tif(self, remote_folder: Path, local_parent: Path) -> Path:
        local_folder = self.download_tif_files(remote_folder, local_parent)
        convert_tif_folder_into_file(local_folder, local_parent)

    def download_tif_files(self, remote_folder: Path, local_parent: Path) -> Path:
        files, folders = self.list_files_and_folder(remote_folder)
        tif_files = self.identify_tifs(files)
        print(f"{len(tif_files)} tif files found in {remote_folder}.")

        if not local_parent.is_dir():
            raise FileNotFoundError(f"{local_parent} does not exist.")
        local_folder = local_parent / remote_folder.name
        if local_folder.is_dir():
            raise FileExistsError(f"{local_folder} already exists.")
        os.mkdir(local_folder)

        print(f"Downloading {len(tif_files)} tif files into {local_folder}.")
        for remote_file in tqdm(tif_files):
            local_file = local_folder / remote_file.name
            self.download_file(remote_file, local_file)
        return local_folder

    @staticmethod
