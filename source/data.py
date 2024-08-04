# data.py
import imageio
import rasterio
import json
import logging
import logger_config
import utils_geo

from rasterio.crs import CRS
from affine import Affine

logger = logging.getLogger(__name__)

def load_data(image_path):
    """
    Load an image from the specified path using imageio.

    Args:
        image_path (str): Path to the image file.

    Returns:
        np.array: Loaded image as a NumPy array.
    """
    img_arr = imageio.v2.imread(image_path)
    logger.info(img_arr.shape)
    return img_arr


def load_geotiff(image_path):
    """
    Load a GeoTIFF file and return the image data and geospatial metadata.

    Args:
        image_path (str): Path to the GeoTIFF file.

    Returns:
        tuple: (image_data, metadata) where image_data is a NumPy array and metadata is a dictionary.

    Longitude:
        - Measures the east-west position on the Earth's surface.
        - Ranges from -180 to 180 degrees.
        - 0 degrees longitude is the Prime Meridian, which passes through Greenwich, England.

    Latitude:
        - Measures the north-south position on the Earth's surface.
        - Ranges from -90 to 90 degrees.
        - 0 degrees latitude is the Equator, which divides the Earth into the Northern and Southern Hemispheres.
    """
    with rasterio.open(image_path) as src:
        image_data = src.read()  # Read all bands

        logger.info(f"Image data is of shape: {image_data.shape}")
        meta_data = src.meta.copy()  # Get metadata
        logger.info(f"Metadata is\n {json.dumps(meta_data, indent=4, cls=CustomEncoder)}")

        # Affine TraFo:
        # [ a, b, c ]
        # [ d, e, f ]
        # [ 0, 0, 1 ]
        # a and e are the pixel size in the x and y directions, respectively.
        # b and d are the row and column rotation (typically these are zero for north-up images).
        # c and f are the x and y coordinates of the upper-left pixel center.

        transform = src.transform  # Get the affine transformation matrix
        crs = src.crs

        x, y = utils_geo.pixel_to_geo(0, 0, transform)
        lon, lat = utils_geo.project_to_geo(x, y, crs)

        logger.info(f"Geographic origin is (lat./lon.): {lat}, {lon}")

        return image_data, meta_data, transform, crs


class CustomEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, CRS):
            return obj.to_string()
        if isinstance(obj, Affine):
            return obj.__dict__
        return super().default(obj)