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
    mov_without_mp4_count = 0
    mov_with_mp4_count = 0
    heic_with_mp4_count = 0
    dirlist_mov_with_mp4s = set()
    dirlist_mov_without_mp4s = set()
    dirlist_heic_to_mp4s = set()

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
            # Computations based on file extension
            ext = Path(file).suffix.lower()
            if Path(file).suffix == "":
                end_notes.append(f"No extension: {root} {file}")
            
            # Keep a set of all seen extensionw
            extensions.add(ext)
            
            # Does it look like a photo, a movie, or ???
            if ext in [".png", ".heic", ".jpg", ".gif", ".dng"]:
                photo_count += 1
            elif ext in [".mov", ".mp4", ".3gp", ".avi"]:
                movie_count += 1
            else:
                end_notes.append(f"Extension not recognized: {root} {dir} {file}")

            # Detect and eliminate files with names that start with "Copy of "
            if file.startswith("Copy of"):
                cleaned_name = file.removeprefix("Copy of ")
                new_name = f"{root}\\{cleaned_name}"
                if os.path.isfile(new_name):
                    error_messages.append(f"Collision: {file} [{cleaned_name}] [{new_name}]")
                    collision_count += 1
                else:
                    try:
                        # Uncomment when you are sure!
                        # #os.rename(f'{root}\\{file}', f'{root}\\{cleaned_name}')
                        end_notes.append(f'SUPPRESSED Rename {root}\\{file} --> {root}\\{cleaned_name}')
                    except:
                        error_messages.append(f'Could not rename in {root}: {file} to {cleaned_name}')

                copy_of_count += 1

            # If it is a .mov or .heic, does it have an identically-named .mp4 (yet)
            if ext == '.mov':
                replacement_file =  file.replace('.MOV','.mp4')
                replacement_file =  replacement_file.replace('.mov','.mp4')
                if os.path.isfile(f'{root}\\{replacement_file}'):
                    dirlist_mov_with_mp4s.add(root)
                    mov_with_mp4_count += 1
                    end_notes.append(f'MOV with mp4: {root}\\{file}')
                else:
                    mov_without_mp4_count += 1
                    dirlist_mov_without_mp4s.add(root)
                    #end_notes.append(f'.MOV without mp4: {root}\\{file}')
            elif ext == '.heic':
                replacement_file =  file.replace('.HEIC','.mp4')
                replacement_file =  replacement_file.replace('.heic','.mp4')
                if os.path.isfile(f'{root}\\{replacement_file}'):
                    dirlist_heic_to_mp4s.add(root)
                    heic_with_mp4_count += 1
                    end_notes.append(f'HEIC with mp4: {root}\\{file}')


    logger.info(f"All extensions seen: {extensions}")
    logger.info(f"Total dirs: {dir_count}")
    logger.info(f"Total files: {file_count}")
    logger.info(f"Total photos: {photo_count}")
    logger.info(f"Total movies: {movie_count}")
    logger.info(f"Total photos+movies: {photo_count + movie_count}")
    logger.info(f"Total mov_with_mp4_count {mov_with_mp4_count}")
    logger.info(f"Total mov_without_mp4_count {mov_without_mp4_count}")
    logger.info(f"Total heic_with_mp4_count {heic_with_mp4_count}")
    logger.info(f'Directories with mov --> mp4 files: {dirlist_mov_with_mp4s}')
    logger.info(f'Directories without mov --> mp4 files: {dirlist_mov_without_mp4s}')
    logger.info(f'Directories with heic --> mp4 files: {dirlist_heic_to_mp4s}')
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
