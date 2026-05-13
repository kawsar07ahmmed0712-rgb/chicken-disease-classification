import json
import base64
import joblib
import yaml

from pathlib import Path
from typing import Any, Dict, List

from box import ConfigBox
from box.exceptions import BoxValueError
from ensure import ensure_annotations

from cnnClassifier import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Read a YAML file and return its content as ConfigBox.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty.
        FileNotFoundError: If the YAML file does not exist.

    Returns:
        ConfigBox: YAML content as ConfigBox.
    """

    try:
        if not path_to_yaml.exists():
            raise FileNotFoundError(f"YAML file not found: {path_to_yaml}")

        with open(path_to_yaml, "r", encoding="utf-8") as yaml_file:
            content = yaml.safe_load(yaml_file)

        if content is None:
            raise ValueError(f"YAML file is empty: {path_to_yaml}")

        logger.info(f"YAML file loaded successfully: {path_to_yaml}")
        return ConfigBox(content)

    except BoxValueError as e:
        logger.error(f"ConfigBox error while reading YAML file: {path_to_yaml}")
        raise ValueError(f"Invalid YAML content in file: {path_to_yaml}") from e

    except yaml.YAMLError as e:
        logger.error(f"YAML parsing error in file: {path_to_yaml}")
        raise e

    except Exception as e:
        logger.error(f"Error occurred while reading YAML file: {path_to_yaml}")
        raise e


@ensure_annotations
def create_directories(path_to_directories: List[Path], verbose: bool = True) -> None:
    """
    Create multiple directories.

    Args:
        path_to_directories (List[Path]): List of directory paths.
        verbose (bool): If True, logs directory creation.
    """

    for path in path_to_directories:
        path.mkdir(parents=True, exist_ok=True)

        if verbose:
            logger.info(f"Directory created or already exists: {path}")


@ensure_annotations
def save_json(path: Path, data: Dict) -> None:
    """
    Save dictionary data into a JSON file.

    Args:
        path (Path): Path to save the JSON file.
        data (Dict): Data to save.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as json_file:
        json.dump(data, json_file, indent=4)

    logger.info(f"JSON file saved successfully: {path}")


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """
    Load JSON file and return its content as ConfigBox.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: JSON content as ConfigBox.
    """

    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")

    with open(path, "r", encoding="utf-8") as json_file:
        content = json.load(json_file)

    logger.info(f"JSON file loaded successfully: {path}")
    return ConfigBox(content)


@ensure_annotations
def save_bin(data: Any, path: Path) -> None:
    """
    Save data as a binary file using joblib.

    Args:
        data (Any): Data to save.
        path (Path): Path to save the binary file.
    """

    path.parent.mkdir(parents=True, exist_ok=True)

    joblib.dump(value=data, filename=path)
    logger.info(f"Binary file saved successfully: {path}")


@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load binary data using joblib.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: Loaded object.
    """

    if not path.exists():
        raise FileNotFoundError(f"Binary file not found: {path}")

    data = joblib.load(path)
    logger.info(f"Binary file loaded successfully: {path}")

    return data


@ensure_annotations
def get_size(path: Path) -> str:
    """
    Get file size in KB.

    Args:
        path (Path): Path of the file.

    Returns:
        str: File size in KB.
    """

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    size_in_kb = round(path.stat().st_size / 1024)
    return f"~ {size_in_kb} KB"


@ensure_annotations
def decode_image(img_string: str, file_name: Path) -> None:
    """
    Decode a Base64 image string and save it as an image file.

    Args:
        img_string (str): Base64 encoded image string.
        file_name (Path): Path where decoded image will be saved.
    """

    file_name.parent.mkdir(parents=True, exist_ok=True)

    image_data = base64.b64decode(img_string)

    with open(file_name, "wb") as image_file:
        image_file.write(image_data)

    logger.info(f"Image decoded and saved successfully: {file_name}")


@ensure_annotations
def encode_image_into_base64(image_path: Path) -> bytes:
    """
    Encode an image file into Base64.

    Args:
        image_path (Path): Path to the image file.

    Returns:
        bytes: Base64 encoded image.
    """

    if not image_path.exists():
        raise FileNotFoundError(f"Image file not found: {image_path}")

    with open(image_path, "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read())

    logger.info(f"Image encoded into Base64 successfully: {image_path}")
    return encoded_image


# Backward-compatible aliases
# Use these only if your old code already calls decodeImage or encodeImageIntoBase64

def decodeImage(imgstring, fileName):
    return decode_image(imgstring, Path(fileName))


def encodeImageIntoBase64(croppedImagePath):
    return encode_image_into_base64(Path(croppedImagePath))