from os import listdir, makedirs, path
from flask import session, request, render_template
from werkzeug.datastructures import FileStorage
from diagnostics.modules.config import SUPPORTED_IMAGE_TYPES, SUPPORTED_AUDIO_TYPES


def get_filepath(subject: str, file: FileStorage, num: int = 0) -> str:
    filename: str = file.filename
    _type: str | None = filename.split(".")[-1] if filename else None
    if _type in SUPPORTED_IMAGE_TYPES:
        binary_file: bytes = file.read()
        return write_image_file(subject=subject, q_num=num, _type=_type, binary=binary_file)
    elif _type in SUPPORTED_AUDIO_TYPES:
        binary_file: bytes = file.read()
        return write_audio_file(subject=subject, _type=_type, binary=binary_file)
    return ""


def get_test_filepath() -> str:
    file: FileStorage = request.files.get("image")
    filename: str = file.filename
    _type: str | None = filename.split(".")[-1] if filename else None
    filepath: str | None = None
    if _type in SUPPORTED_IMAGE_TYPES:
        filepath: str = write_test_image(_type, file.read())

    return filepath


def write_image_file(subject: str, q_num: int, _type: str, binary: bytes) -> str:
    if not path.exists(f"diagnostics/static/images/{subject}"):
        makedirs(f"diagnostics/static/images/{subject}", mode=0o700)
    images_count: int = len(listdir(f"diagnostics/static/images/{subject}"))
    filepath: str = f"diagnostics/static/images/{subject}/q_{q_num}_{images_count + 1}.{_type}"
    print(filepath)
    with open(filepath, "wb") as image:
        image.write(binary)
    return filepath[11:]


def write_test_image(_type: str, binary: bytes) -> str:
    if not path.exists(f"diagnostics/static/images/test"):
        makedirs(f"diagnostics/static/images/test", mode=0o700)
    images_count: int = len(listdir("diagnostics/static/images/test"))
    filepath: str = f"diagnostics/static/images/test/test_{images_count + 1}.{_type}"

    with open(filepath, "wb") as test_image:
        test_image.write(binary)
    return filepath[11:]


def write_audio_file(subject: str, _type: str, binary: bytes) -> str:
    if not path.exists(f"diagnostics/static/audio/{subject}"):
        makedirs(f"diagnostics/static/audio/{subject}", mode=0o700)
    images_count: int = len(listdir(f"diagnostics/static/audio/{subject}"))
    filepath: str = f"diagnostics/static/audio/{subject}/q_audio_{images_count + 1}.{_type}"
    with open(filepath, "wb") as image:
        image.write(binary)
    return filepath[11:]