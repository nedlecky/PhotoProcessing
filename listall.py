import logging

logger = logging.getLogger(__name__)
import time

import os
from pathlib import Path


def list_all_files(directory):
    logger.info("starts")

    dir_count = 0

    file_count = 0
    photo_count = 0
    movie_count = 0

    copy_of_count = 0
    collision_count = 0
    extensions = set()

    end_notes = []
    error_messages = []

    for root, dirs, files in os.walk(directory):
        dir_count += len(dirs)
        file_count += len(files)

        if len(dirs) < 1:
            logger.info(f"{root}  {len(files)} files")
        else:
            logger.info(f"{root}  {len(dirs)} dirs  {len(files)} files")

        for file in files:
            ext = Path(file).suffix
            if Path(file).suffix == "":
                end_notes.append(f"No extension: {root} {file}")
            extensions.add(ext)
            if ext.lower() in [".png", ".heic", ".jpg", ".gif", ".dng"]:
                photo_count += 1
            elif ext.lower() in [".mov", ".mp4", ".3gp", ".avi"]:
                movie_count += 1
            else:
                end_notes.append(f"Extension not recognized: {root} {dir} {file}")

            if file.startswith("Copy of"):
                cleaned_name = file.removeprefix("Copy of ")
                new_name = f"{root}\\{cleaned_name}"
                if os.path.isfile(new_name):
                    error_messages.append(f"Collision: {file} [{cleaned_name}] [{new_name}]")
                    collision_count += 1
                else:
                    try:
                        os.rename(f'{root}\\{file}', f'{root}\\{cleaned_name}')
                        end_notes.append(f'Renamed {root}\\{file} --> {root}\\{cleaned_name}')
                    except:
                        error_messages.append(f'Could not rename in {root}: {file} to {cleaned_name}')

                    #os.path.re
                copy_of_count += 1

    logger.info(f"All extensions seen: {extensions}")
    logger.info(f"Total dirs: {dir_count}")
    logger.info(f"Total files: {file_count}")
    logger.info(f"Total photos: {photo_count}")
    logger.info(f"Total movies: {movie_count}")
    logger.info(f"Total photos+movies: {photo_count + movie_count}")
    logger.info(f'Total "Copy of..." files: {copy_of_count}')
    logger.info(f"Total collision count: {collision_count}")
    logger.info(f"{len(end_notes)} end_notes")
    for line in end_notes:
        logger.info(line)
    logger.info(f"{len(error_messages)} error_messages")
    for line in error_messages:
        logger.info(line)

    logger.info("ends")


def subfunc(x):
    logger.info("starts")
    time.sleep(0.1)
    logger.info("ends")


def listall():
    logger.info("starts")
    subfunc(123)
    time.sleep(0.1)
    logger.info("ends")


if __name__ == "__main__":
    # Set the default log level
    logger.setLevel(logging.DEBUG)

    # Create handlers
    c_handler = logging.StreamHandler()  # Console handler
    f_handler = logging.FileHandler("photoproc.log")  # File handler

    # Set log levels for handlers
    c_handler.setLevel(logging.DEBUG)
    f_handler.setLevel(logging.DEBUG)

    # Create formatters and add them to handlers
    c_format = logging.Formatter(
        datefmt="%H:%M:%S",
        style="{",
        fmt="{asctime}.{msecs},{levelname},{name},{module}.{funcName}:{lineno},{message}",
    )
    f_format = logging.Formatter(
        datefmt="%Y-%m-%d,%H:%M:%S",
        style="{",
        fmt="{asctime}.{msecs},{levelname},{name},{module}.{funcName}:{lineno},{message}",
    )
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    # Example usage
    logger.debug("This is a debug message")
    logger.info("This is an info message")
    logger.warning("This is a warning message")
    logger.error("This is an error message")
    logger.critical("This is a critical message")

    """
    logging.basicConfig(
        filename="photoproc.log",
        level=logging.DEBUG,
        style="{",
        format="{asctime}.{msecs},{levelname},{module}.{funcName}:{lineno},{name},{message}",
        datefmt="%Y-%m-%d,%H:%M:%S",
    )
    """

    print("Test code running...")
    logger.info("Test code running...")
    listall()

    list_all_files("C:\\Users\\nedlecky\\ACDSee")

    logging.shutdown()
