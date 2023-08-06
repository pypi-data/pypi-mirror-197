"""Basic connection to a nas."""
import os
from pathlib import Path

import pysftp
from tqdm import tqdm


class SftpConnection:
    def __init__(self, host_name: str, user_name: str, pwd: str) -> None:
        self.connection: pysftp.Connection = pysftp.Connection(
            host=host_name,
            username=user_name,
            password=pwd,
        )
        print(f"Connection established: {host_name}@{user_name}")

    def close(self) -> None:
        self.connection.close()

    def list_contents(self, remote_folder: Path) -> list[Path]:
        if not self.connection.isdir(str(remote_folder)):
            raise FileNotFoundError(f"{remote_folder} not found.")

        contents: list[str] = self.connection.listdir(str(remote_folder))
        contents: list[Path] = [remote_folder / name for name in contents]
        return contents

    def list_files_and_folder(self, remote_folder: Path) -> tuple:
        files = []
        folders = []

        contents = self.list_contents(remote_folder)
        for element in contents:
            if self.connection.isfile(str(element)):
                files.append(element)
            elif self.connection.isdir(str(element)):
                folders.append(element)
            else:
                raise ValueError(f"{element} is neither file nor folder?")

        return files, folders

    def download_file(self, remote_file: Path, local_file: Path) -> None:
        if not self.connection.isfile(str(remote_file)):
            raise FileNotFoundError(f"{remote_file} does not exist.")
        if not local_file.parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_file.parent} does not exist.")
        if local_file.is_file():
            raise FileExistsError(f"{local_file} already exists.")
        self.connection.get(str(remote_file), str(local_file))

    def upload_file(self, local_file: Path, remote_file: Path) -> None:
        if not local_file.is_file():
            raise FileNotFoundError(f"{local_file} does not exist.")
        if not self.connection.isdir(str(remote_file.parent)):
            raise FileNotFoundError(f"Target parent folder {remote_file.parent} does not exist.")
        if self.connection.isfile(str(remote_file)):
            raise FileExistsError(f"{remote_file} already exists.")
        self.connection.put(str(local_file), str(remote_file))

    def download_folder(self, remote_folder: Path, local_parent: Path, recursive: bool = True) -> Path:
        if not self.connection.isdir(str(remote_folder)):
            raise FileNotFoundError(f"{remote_folder} does not exist.")
        if not local_parent.is_dir():
            raise FileNotFoundError(f"Target parent folder {local_parent} does not exist.")

        local_folder = local_parent / remote_folder.name
        if local_folder.is_dir():
            raise FileExistsError(f"{local_folder} already exists.")
        os.mkdir(local_folder)

        files, folders = self.list_files_and_folder(remote_folder)
        print(f"{len(files)} files found in {remote_folder}.")
        print(f"{len(folders)} folders found in {remote_folder}.")
        for remote_file in tqdm(files):
            local_file = local_folder / remote_file.name
            self.download_file(remote_file, local_file)

        if recursive:
            for remote_sub_folder in folders:
                self.download_folder(remote_sub_folder, local_folder, recursive=recursive)
        return local_folder

    def upload_folder(self, local_source: Path, remote_target: Path) -> None:
        raise NotImplementedError()

    def print_tree(self, remote_folder: Path, recursive: bool = True, level: int = 0, max_level: int = 3) -> None:
        if level < max_level:
            files, folders = self.list_files_and_folder(remote_folder)
            indent = f"\t" * level
            for file in files:
                print(f"{indent} {file.name}")

            for folder in folders:
                print(f"{indent} {folder.name}")
                if recursive:
                    self.print_tree(folder, level=level + 1, max_level=max_level)
