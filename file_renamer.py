import logging

logger = logging.getLogger(__name__)
import time

import os
from pathlib import Path

def file_renamer(directory):
    logger.info("starts")

    dir_count = 0

    file_count = 0
    photo_count = 0
    movie_count = 0

    extensions = set()
    unique_filenames = set()
    extensions_of_duplicates = set()

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
            # Computations based on file extension
            ext = Path(file).suffix.lower()
            if Path(file).suffix == "":
                end_notes.append(f"No extension: {root} {file}")

            # Keep a set of all seen extensions
            extensions.add(ext)

            # Checks for unique filenames
            if file in unique_filenames:
                #end_notes.append(f'dup {ext} filename {root}\\{file}')
                extensions_of_duplicates.add(ext)
            else:
                unique_filenames.add(file)

            def renamer(file, old_prefix, new_prefix):
                if file.startswith(old_prefix):
                    replaced_name = file.replace(old_prefix, new_prefix)
                    new_name = f"{root}\\{replaced_name}"
                    old_name = f"{root}\\{file}"
                    end_notes.append(f"Suggest rename: {old_name} --> {new_name}")
                    #os.rename(old_name, new_name)

            # Rename 2024-06-27(nn) to IMG1_(nn), etc.
            renamer(file, '2024-06-26', 'IMG0_')
            renamer(file, '2024-06-27', 'IMG1_')
            renamer(file, '2024-06-28', 'IMG2_')
            renamer(file, '2024-07-01', 'IMG3_')
            renamer(file, '2024-07-02', 'IMG4_')
            renamer(file, '2024-07-07', 'IMG5_')
            renamer(file, '2024-07-03', 'IMG6_')
            renamer(file, '2024-07-06', 'IMG7_')
            renamer(file, '2024-07-08', 'IMG8_')
            
            # Does it look like a photo, a movie, or ???
            if ext in [".png", ".heic", ".jpg", ".gif", ".dng"]:
                photo_count += 1
            elif ext in [".mov", ".mp4", ".3gp", ".avi"]:
                movie_count += 1
            else:
                end_notes.append(f"Extension not recognized: {root} {dir} {file}")

    logger.info(f"All extensions seen: {extensions}")
    logger.info(f"Total dirs: {dir_count}")
    logger.info(f"Total files: {file_count}")
    logger.info(f"Total unique filenames: {len(unique_filenames)}")
    logger.info(f"Extensions of duplicate filenames: {extensions_of_duplicates}")
    logger.info(f"Total photos: {photo_count}")
    logger.info(f"Total movies: {movie_count}")
    logger.info(f"Total photos+movies: {photo_count + movie_count}")
    logger.info(f"{len(end_notes)} end_notes")
    for i, line in enumerate(end_notes, start=1):
        logger.info(f'{i}: {line}')
    logger.info(f"{len(error_messages)} error_messages")
    for i, line in enumerate(error_messages, start=1):
        logger.info(f'{i}: {line}')

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

    file_renamer("C:\\Users\\nedlecky\\ACDSee")

    logging.shutdown()
