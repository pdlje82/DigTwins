# main.py
from data import load_data, load_geotiff
import torch_img
import logging
import logger_config

logger = logging.getLogger(__name__)

img_path = "/mnt/e/Satellite_Imagery/baa9e191_img_pneo3_202306170843064_pms-fs_ort_68ebce5f-4089-4a17-cad1-6219897f9bb3_ned.tiff"


def main():
    # Specify the path to the image

    # Load the image
    image = load_data(img_path)

    image, metadata, transform, crs = load_geotiff(img_path)
    # copy image to pytorch tensor
    my_torch_ortho_img = torch_img.TorchOrthoImage(image)

if __name__ == "__main__":
    main()
