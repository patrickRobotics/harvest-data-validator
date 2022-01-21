import json

import numpy as np
import pandas as pd

from data_validator import (
    FARM_DISTANCE_VIOLATION, WET_WEIGHT_VIOLATION, DRY_WEIGHT_SD_VIOLATION,
    DUPLICATE_PHOTOS_VIOLATION, MULTIPLE_MEASUREMENTS_VIOLATION, ERRORS
)
from data_validator.helpers.utils import get_farm_distances


class FarmDataValidator:
    def __init__(self, data="", images=""):
        self._data = data
        self._images = images

    def _get_harvest_measurements(self):
        return self._data

    def _get_images_data(self):
        return self._images

    def _set_harvest_measurements(self, data):
        self._data = data

    def _set_images_data(self, images):
        self._images = images

    @staticmethod
    def _format_response(data_point: list, violated_rule: str) -> dict:
        """Formats response for farm data validator."""

        if not data_point and not violated_rule:
            raise Exception("Please provide processed data and violation rule")
        return json.dumps({"violated_rule": violated_rule, "data_point": data_point})

    def validate_multiple_measurements_for_one_crop(self) -> dict:
        """Returns data points that violate multiple measurements for the same crop in a single farm rule."""

        data = self._get_harvest_measurements()
        multiple_measurements = []
        dataframe = pd.DataFrame(data)
        grouped_dataframe = dataframe.groupby(["farm_id", "crop"], as_index=False).size()
        multiple_entries = grouped_dataframe.loc[grouped_dataframe["size"] > 1]
        multiple_entries_dict = multiple_entries.to_dict("records")

        for i in range(len(multiple_entries_dict)):
            row_series = dataframe[
                dataframe["farm_id"] == multiple_entries_dict[i]["farm_id"]
            ]
            multiple_measurements += row_series.to_dict("records")

        return FarmDataValidator._format_response(
            data_point=multiple_measurements,
            violated_rule=ERRORS[MULTIPLE_MEASUREMENTS_VIOLATION],
        )

    def validate_weights(self) -> dict:
        """Returns data points where dry weight measurement exceeds the corresponding wet weight measurement"""
        invalid_data_points = []
        data = self._get_harvest_measurements()

        for i in range(len(data)):
            wet_weight = data[i]["wet_weight"]
            dry_weight = data[i]["dry_weight"]

            invalid_data_point = {
                key: value
                for (key, value) in data[i].items() if dry_weight > wet_weight
            }

            if bool(invalid_data_point):
                invalid_data_points.append(invalid_data_point)

        return FarmDataValidator._format_response(
            data_point=invalid_data_points,
            violated_rule=ERRORS[WET_WEIGHT_VIOLATION],
        )

    def validate_dry_weight_deviations(self) -> dict:
        """
        Returns data points where dry weights is outside the standard deviation of
        all other submissions for the same crop
        """
        invalid_data_points = []
        data = self._get_harvest_measurements()
        dry_weights = [
            data[i]["dry_weight"] for i in range(len(data))
        ]

        dry_weight_std = np.std(dry_weights, axis=0)
        dry_weight_mean = np.mean(dry_weights, axis=0)
        positive_one_std_mean = dry_weight_mean + 1 * dry_weight_std
        negative_one_std_mean = dry_weight_mean - 1 * dry_weight_std

        for i in range(len(data)):
            dry_weight = data[i]["dry_weight"]
            invalid_data_point = {
                key: value
                for (key, value) in data[i].items()
                if dry_weight < negative_one_std_mean or dry_weight > positive_one_std_mean
            }

            if bool(invalid_data_point):
                invalid_data_points.append(invalid_data_point)
        return FarmDataValidator._format_response(
            data_point=invalid_data_points,
            violated_rule=ERRORS[DRY_WEIGHT_SD_VIOLATION],
        )

    def validate_photos(self) -> dict:
        """Returns images that violate duplicate photo submission"""
        images_data = self._get_images_data()
        duplicate_images = []
        unique = set()
        duplicates = [x for x in images_data if x in unique or unique.add(x)]
        if len(duplicates) > 0:
            for img in duplicates:
                duplicate_images.append(img)

            return FarmDataValidator._format_response(
                data_point=duplicate_images,
                violated_rule=ERRORS[DUPLICATE_PHOTOS_VIOLATION],
            )

    def validate_farm_distances(self):
        """Returns data points where GPS coordinates of one farm are within 200 meters of another recorded farm"""
        invalid_data_points = []
        seen = set()

        data = self._get_harvest_measurements()
        for i in range(len(data)):
            coord_1 = tuple(map(float, data[i]["location"].split(', ')))
            for loc in range(len(data)):
                coord_2 = tuple(map(float, data[loc]["location"].split(', ')))
                distance = get_farm_distances(coord_1, coord_2)
                if 200 > distance > 0:
                    seen.add((data[i]["farm_id"], data[loc]["farm_id"]))

        for entry in seen:
            farm_1 = list(filter(lambda farm: farm['farm_id'] == entry[0], data))[0]
            farm_2 = list(filter(lambda farm: farm['farm_id'] == entry[1], data))[0]
            invalid_data_points.append("[{} ** is near ** {}]".format(farm_1, farm_2))

        return FarmDataValidator._format_response(
                data_point=invalid_data_points,
                violated_rule=ERRORS[FARM_DISTANCE_VIOLATION],
            )

