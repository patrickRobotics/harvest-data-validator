"""Top-level package for Python Harvest Data Validator."""
# data_validator/__init__.py

__app_name__ = "harvest-data_validator"
__version__ = "0.1.0"

(
    SUCCESS,
    DISTANCE_ERROR,
    DIR_ERROR,
    FILES_ERROR,
    JSON_ERROR,
    IMAGE_ERROR,
    FARM_DISTANCE_VIOLATION,
    WET_WEIGHT_VIOLATION,
    DRY_WEIGHT_SD_VIOLATION,
    DUPLICATE_PHOTOS_VIOLATION,
    MULTIPLE_MEASUREMENTS_VIOLATION,
) = range(11)

ERRORS = {
    DIR_ERROR: "data directory error",
    FILES_ERROR: "parsing directory files error",
    JSON_ERROR: "error parsing json file",
    IMAGE_ERROR: "error processing image file",
    DISTANCE_ERROR: "error getting Euclidean Distances between farms",
    FARM_DISTANCE_VIOLATION: "GPS coordinates of farm within 200 meters of another recorded farm",
    WET_WEIGHT_VIOLATION: "Dry weight measurement exceeds the corresponding wet weight measurement",
    DRY_WEIGHT_SD_VIOLATION: "Dry weight is outside SD of all other submissions for the same crop",
    DUPLICATE_PHOTOS_VIOLATION: "Photo submitted is a duplicate of another photo that was submitted",
    MULTIPLE_MEASUREMENTS_VIOLATION: "Multiple measurements for the same crop in a single farm",
}
