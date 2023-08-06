from pathlib import Path

import numpy as np
import tifffile
from tqdm import tqdm


def list_files_and_folders(local_folder: Path) -> tuple:
    contents = local_folder.iterdir()
    files = []
    folders = []
    for element in contents:
        if element.is_file():
            files.append(element)
        elif element.is_dir():
            folders.append(element)
        else:
            raise ValueError(f"{element} is neither file nor folder?")
    return files, folders


def identify_tifs(files: list[Path]) -> list:
    tif_files = []
    for file in files:
        if file.suffix == ".tif":
            tif_files.append(file)
    return tif_files


def convert_tif_folder_into_file(source_folder: Path, target_parent: Path) -> Path:
    if not source_folder.is_dir():
        raise FileNotFoundError(f"{source_folder} does not exist.")
    if not target_parent.is_dir():
        raise FileNotFoundError(f"{target_parent} does not exist.")

    target_file = target_parent / f"{source_folder.name}.tif"
    if target_file.is_file():
        raise FileExistsError(f"{target_file} already exists.")

    tifs = list_tifs(source_folder)
    print(f"{len(tifs)} found in {source_folder}.")
    sorted_tifs = sort_tifs(tifs)
    print(f"Loading {sorted_tifs.size} tifs.")
    movie = load_tifs(sorted_tifs)
    print(f"Tifs loaded into movie with shape {movie.shape}.")
    print(f"Saving movie to {target_file}.")
    write_movie_to_tif(movie, target_file)
    return target_file


def list_tifs(local_folder: Path) -> list:
    files, _ = list_files_and_folders(local_folder)
    tif_files = identify_tifs(files)
    return tif_files


def write_movie_to_tif(movie: np.ndarray, target_file: Path) -> None:
    tifffile.imwrite(target_file, data=movie, bigtiff=True)


def load_tifs(tif_files: list[Path], dtype=np.uint8) -> np.ndarray:
    list_of_images = []
    for file in tqdm(tif_files):
        image = tifffile.imread(file).astype(dtype)
        list_of_images.append(image)
    movie = np.stack(list_of_images, axis=0)
    return movie


def sort_tifs(tif_files: list[Path]) -> np.ndarray[Path]:
    file_names = [file.name for file in tif_files]
    sort_vector = np.argsort(file_names)
    sorted_files = np.asarray(tif_files)[sort_vector]
    return sorted_files


if __name__ == "__main__":
    SOURCE_FOLDER = Path("/home/mathis/Code/gitlab/labnas/data/mapping_with_shielding")
    TARGET_PARENT = Path("/home/mathis/Code/gitlab/labnas/data/")
    convert_tif_folder_into_file(SOURCE_FOLDER, TARGET_PARENT)