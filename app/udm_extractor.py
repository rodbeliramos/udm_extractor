import sys
import rasterio as rio
from pathlib import Path

proj_folder = Path(__file__).parents[1].resolve()
sys.path.append(str(proj_folder))


def udm_band_extraction(raster_src:Path, dst_folder:Path, band:int) -> None:
    """
    Create a new raster file on destiny folder by extracting a selected band
    :param Path raster_src:     full path of raster file
    :param Path dst_folder:     full path where to create extracted udm files
    :param int band:            level of target band on raster_src
    :returns:                   None
    """
    # Open udm2 raster file
    with rio.open(raster_src) as udm2_file:
        udm = udm2_file.read(band)

    # Create new udm raster file on dst_folder
    with rio.open(dst_folder.joinpath(str(raster_src.name).replace('udm2', 'udm')),
                  'w',
                  driver='GTiff',
                  height=udm.shape[0],
                  width=udm.shape[1],
                  count=1,
                  dtype=udm.dtype,
                  crs='+proj=latlong',
                  transform=udm2_file.transform) as udm_file:
        udm_file.write(udm, 1)
    return


if __name__ == '__main__':
    # Band level where UDM is located
    UDM_BAND = 8
    # source folder - Put raster and udm2 files on this folder
    src_path = proj_folder.joinpath('data/input')
    # destiny folder - Folder
    dst_path = proj_folder.joinpath('data/output')
    # list all udm2 files
    suffixes = ['**/*udm2*.tif', '**/*udm2*.tiff']
    udm2_files = []
    for suffix in suffixes:
        udm2_files.extend(src_path.rglob(suffix))

    # extract udm band and create new file
    for udm2_file in udm2_files:
        udm_band_extraction(udm2_file, dst_path, UDM_BAND)
