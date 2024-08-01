import logging

logger = logging.getLogger(__name__)

import time
import os
from pathlib import Path
from PIL import Image
import exifread
import re


def adjust_metadata(directory):
    logger.info("starts")

    dir_count = 0
    file_count = 0
    photo_count = 0
    png_count = 0
    heic_count = 0
    movie_count = 0
    filename_date_checked = 0
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

        num_str = re.findall(r"[0-9]{4}", root)
        min_year = 1900
        max_year = 2100
        if len(num_str) >= 2:
            try:
                min_year = int(num_str[0])
                max_year = int(num_str[1])
            except:
                pass
        elif len(num_str) == 1:
            try:
                min_year = int(num_str[0])
                max_year = min_year
            except:
                pass

        logger.info(f"{min_year=} {max_year=}")

        if "[Originals]" in root:
            end_notes.append(f"Originals: {root}")

        for file in files:
            full_name = f"{root}\\{file}"

            # Computations based on file extension
            ext = Path(file).suffix.lower()
            if Path(file).suffix == "":
                end_notes.append(f"No extension: {root} {file}")

            # Keep a set of all seen extensions
            extensions.add(ext)

            # Does it look like a photo, a movie, or ???
            if ext in [".png", ".heic", ".jpg", ".gif", ".dng"]:
                photo_count += 1
                """
                if ext != '.heic' and photo_count < 2:
                    full_name = f'{root}\\{file}'
                    try:
                        image = Image.open(full_name)
                        print(image.format)
                        count += 1
                    except:
                        error_messages.append(f'Image could not open {full_name}')
                """
                # WORKS!
                # if min_year >= 1900 and max_year <= 2024:
                if min_year >= 1900 and max_year <= 2024:
                    if ext == ".png":
                        png_count += 1
                    else:
                        if ext == ".heic":
                            heic_count += 1
                            continue

                        # Open image file for reading (binary mode)
                        tag_year = 0
                        try:
                            with open(full_name, "rb") as f:
                                # Return Exif tags
                                tags = exifread.process_file(f)
                                # Gets 2007:11:19 09:53:49
                                tag = tags["EXIF DateTimeOriginal"]

                                tag_year = int(str(tag)[0:4])
                                tag_month = int(str(tag)[5:7])
                                tag_day = int(str(tag)[8:10])
                                if tag_year < min_year or tag_year > max_year:
                                    error_messages.append(
                                        f"{tag_year} out of year range {min_year}-{max_year}: {full_name}"
                                    )

                                # Find all 19yymmdd or 20yymmdd in the text
                                # (19\d{2}|20\d{2}) - Matches exactly four digits representing the year 19XX or 20XX
                                # (0[1-9]|1[0-2]) - Matches a two-digit month, allowing values from 01 to 12
                                # (0[1-9]|[12][0-9]|3[01]) - Matches a two-digit day, allowing values from 01 to 31.
                                pattern = (
                                    r"(19\d{2}|20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])"
                                )
                                matches = re.findall(pattern, file)
                                if len(matches) == 1:
                                    if len(matches[0]) == 3:
                                        filename_date_checked += 1
                                        name_year = int(matches[0][0])
                                        name_month = int(matches[0][1])
                                        name_day = int(matches[0][2])
                                        #end_notes.append(
                                        #    f"{matches} {name_year} {name_month} {name_day} {root} {file}"
                                        #)
                                        # Name matches tag??
                                        #if name_year < min_year or name_year > max_year:
                                        if name_year != tag_year or name_month != tag_month or name_day != tag_day:
                                            error_messages.append(
                                                f"{name_year} filename pattern doesn't match EXIF: {tag} {matches[0]} {full_name}"
                                            )

                        except:
                            error_messages.append(
                                f"Exifread could not handle {full_name} {tag} {tag_year=}"
                            )

            elif ext in [".mov", ".mp4", ".3gp", ".avi"]:
                movie_count += 1

                # No EXIF for movies, but we can check any dates embedded in filenames against the folder name years!

                # These are all fine for years 2000-2024
                # Find all 19yymmdd or 20yymmdd in the text
                # (19\d{2}|20\d{2}) - Matches exactly four digits representing the year 19XX or 20XX
                # (0[1-9]|1[0-2]) - Matches a two-digit month, allowing values from 01 to 12
                # (0[1-9]|[12][0-9]|3[01]) - Matches a two-digit day, allowing values from 01 to 31.
                pattern = (
                    r"(19\d{2}|20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12][0-9]|3[01])"
                )
                matches = re.findall(pattern, file)
                if len(matches) == 1:
                    if len(matches[0]) == 3:
                        filename_date_checked += 1
                        name_year = int(matches[0][0])
                        name_month = int(matches[0][1])
                        name_day = int(matches[0][2])
                        #end_notes.append(
                        #   f"{matches} {name_year} {name_month} {name_day} {root} {file}"
                        #)
                        if name_year < min_year or name_year > max_year:
                            error_messages.append(
                                f"{name_year} filename date out of year range {min_year}-{max_year}: {full_name}"
                            )

            else:
                end_notes.append(f"Extension not recognized: {root} {dir} {file}")

    logger.info(f"All extensions seen: {extensions}")
    logger.info(f"Total dirs: {dir_count}")
    logger.info(f"Total files: {file_count}")
    logger.info(f"Total photos: {photo_count}")
    logger.info(f"Total png: {png_count}")
    logger.info(f"Total heic: {heic_count}")
    logger.info(f"Total movies: {movie_count}")
    logger.info(f"Total photos+movies: {photo_count + movie_count}")
    logger.info(f"Total filename_date checked: {filename_date_checked}")
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

    adjust_metadata("C:\\Users\\nedlecky\\ACDSee")

    logging.shutdown()
