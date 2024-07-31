import logging
logger = logging.getLogger(__name__)

import time
import os
from pathlib import Path
from PIL import Image
import exifread


def adjust_metadata(directory):
    logger.info("starts")

    dir_count = 0
    file_count = 0
    photo_count = 0
    movie_count = 0
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
                '''
                if ext != '.heic' and photo_count < 2:
                    full_name = f'{root}\\{file}'
                    try:
                        image = Image.open(full_name)
                        print(image.format)
                        count += 1
                    except:
                        error_messages.append(f'Image could not open {full_name}')
                '''
                if True: #photo_count < 1000:
                    # Open image file for reading (binary mode)
                    full_name = f'{root}\\{file}'
                    try:
                        with open(full_name, 'rb') as f:
                            # Return Exif tags
                            tags = exifread.process_file(f)

                            # Print the tags
                            #for tag in tags.keys():
                            #    print(f"{tag}: {tags[tag]}")
                            print(tags['EXIF DateTimeOriginal'])
                    except:
                        error_messages.append(f'Exifread could not handle {full_name}')

            elif ext in [".mov", ".mp4", ".3gp", ".avi"]:
                movie_count += 1
            else:
                end_notes.append(f"Extension not recognized: {root} {dir} {file}")
   

    logger.info(f"All extensions seen: {extensions}")
    logger.info(f"Total dirs: {dir_count}")
    logger.info(f"Total files: {file_count}")
    logger.info(f"Total photos: {photo_count}")
    logger.info(f"Total movies: {movie_count}")
    logger.info(f"Total photos+movies: {photo_count + movie_count}")
    logger.info(f"{len(end_notes)} end_notes")
    for line in end_notes:
        logger.info(line)
    logger.info(f"{len(error_messages)} error_messages")
    for line in error_messages:
        logger.info(line)

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

    adjust_metadata("C:\\Users\\nedlecky\\ACDSee")

    logging.shutdown()
