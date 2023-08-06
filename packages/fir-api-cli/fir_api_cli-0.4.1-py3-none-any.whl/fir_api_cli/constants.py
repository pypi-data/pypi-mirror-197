from pathlib import Path

FIR_API_URL = "https://api.fir.gov.hu/api"

RETURN_ITEMS_SHORT = [
    'id',
    'filename',
    'downloadUrl',
    'size'
]

RETURN_ITEMS_LONG = [
    *RETURN_ITEMS_SHORT,
    'collection',
    'productType',
    'cloudCoverPercentage',
    'footprint',
    'processingDate',
    'beginPosition',
    'endPosition',
    'tileIdentifier',
    'relativeOrbitNumber',
]

(
    SUCCESS,
    FILE_ERROR,
    JSON_ERROR
) = range(3)

ERRORS = {
    FILE_ERROR: "file read/write error",
}
DEFAULT_CONFIG_FILE_PATH = Path.home() / '.fir/config'
