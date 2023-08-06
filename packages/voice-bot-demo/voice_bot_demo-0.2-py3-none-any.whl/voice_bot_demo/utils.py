import os


def file_relative_path(dunderfile: str, relative_path: str) -> str:
    return os.path.join(os.path.dirname(dunderfile), relative_path)
