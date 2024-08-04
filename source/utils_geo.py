import logging
from affine import Affine
from pyproj import Transformer

logger = logging.getLogger(__name__)


def pixel_to_geo(pixel_row, pixel_col, transform):
    """
    Convert pixel coordinates to geographic coordinates.

    Args:
        pixel_row (int): The row (height) coordinate of the pixel.
        pixel_col (int): The column (width) coordinate of the pixel.
        transform (Affine): The affine transformation matrix.

    Returns:
        tuple: (longitude, latitude) geographic coordinates.
    """
    # Apply the affine transformation to the pixel coordinates
    x, y = transform * (pixel_col, pixel_row)
    return x, y

def project_to_geo(x, y, src_crs, dst_crs='EPSG:4326'):
    """
    Convert projected coordinates to geographic coordinates (latitude, longitude).

    Args:
        x (float): Projected x coordinate.
        y (float): Projected y coordinate.
        src_crs (str): Source CRS.
        dst_crs (str): Destination CRS, default is 'EPSG:4326' (WGS84).

    Returns:
        tuple: (longitude, latitude) geographic coordinates.
    """
    transformer = Transformer.from_crs(src_crs, dst_crs, always_xy=True)
    lon, lat = transformer.transform(x, y)
    return lon, lat