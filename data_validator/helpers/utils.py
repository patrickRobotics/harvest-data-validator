import os
import json
import haversine as hs
from haversine import Unit
from math import floor
from pathlib import Path

from data_validator import FILES_ERROR, JSON_ERROR, IMAGE_ERROR, DISTANCE_ERROR

ALLOWED_FILE_TYPES_EXTENSIONS = (".json", ".jpg", ".png")


def get_folder_files(path: str) -> list:
    """Returns files from the provided folder"""
    dir_files = []
    for subdir, dirs, files in os.walk(path):
        if len(files) == 0:
            return FILES_ERROR
        for filename in files:
            filepath = subdir + os.sep + filename
            if filepath.endswith(ALLOWED_FILE_TYPES_EXTENSIONS):
                dir_files.append(filepath)

    return dir_files


def get_data_from_json_file(file_path: str) -> list:
    """Returns the json object containing harvest_measurements data points"""
    try:
        with open(file_path, "r") as farm_data:
            data = json.load(farm_data)
            return data["harvest_measurements"]
    except IOError:
        return JSON_ERROR


def get_farm_images(file_path: str) -> object:
    """Returns image file if the file is one of the allowed image formats"""

    if Path(file_path).suffix in ('.png', '.jpg', '.jpeg'):
        file_name = file_path.rpartition('/')
        return file_name[2]
    else:
        return IMAGE_ERROR


def get_farm_distances(location_one: tuple, location_two: tuple) -> float:
    """ Returns distance between two farms given their longitudes and latitudes"""
    try:
        distance = hs.haversine(location_one, location_two,unit=Unit.METERS)
        return floor(distance)
    except Exception as e:
        return DISTANCE_ERROR
