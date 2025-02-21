import logging
import os
import shutil
import sys


def rel(path: str) -> str:
    return os.path.relpath(path)


def get_logger() -> logging.Logger:
    logging.basicConfig(
        stream=sys.stdout,
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(__name__)


def copy_tree_recursive(current_src: str, current_dst: str) -> None:
    logger = get_logger()
    os.makedirs(current_dst, exist_ok=True)
    for branch in os.listdir(current_src):
        src_path = os.path.join(current_src, branch)
        dst_path = os.path.join(current_dst, branch)
        if os.path.isfile(src_path):
            shutil.copy2(src_path, dst_path)
            logger.info(f'Copied file: "{rel(src_path)}" to "{rel(dst_path)}"')
        elif os.path.isdir(src_path):
            copy_tree_recursive(src_path, dst_path)


def copytree(src_dir: str, dst_dir: str) -> None:
    logger = get_logger()

    if not os.path.exists(src_dir):
        raise FileNotFoundError(f'Source directory "{rel(src_dir)}" does not exist')

    if os.path.exists(dst_dir):
        try:
            shutil.rmtree(dst_dir)
            logger.info(f'Cleaned up directory: "{rel(dst_dir)}"')
        except PermissionError as e:
            raise PermissionError(
                f'Permission denied while deleting "{rel(dst_dir)}": {e}'
            ) from e
        except OSError as e:
            raise OSError(f'Failed to delete "{rel(dst_dir)}": {e}') from e

    copy_tree_recursive(src_dir, dst_dir)
    logger.info(f'Copied directory: "{rel(src_dir)}" to "{rel(dst_dir)}"')
