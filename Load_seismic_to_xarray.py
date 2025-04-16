"""
Near and far offset partial stacks: subcubes from full 3-d cubes.
segy format

* inline: 1300-1500, every 2
* xline: 1500-2000, every 2
* time: 1500-2500 ms
* total 25351 traces for each subcube.

* xline number stored in bytes 21-26.
* inline number (multiplied by 1000) stored in bytes 41-44.

"""



import matplotlib.pyplot as plt
import pathlib
from segysak.segy import get_segy_texthead
from segysak.segy import segy_header_scan
import pandas as pd
from segysak.segy import segy_header_scrape
import xarray as xr

segy_path = pathlib.Path("Seismic/3d_nearstack.sgy")
print("3D", segy_path, segy_path.exists())

get_segy_texthead(segy_path)

scan = segy_header_scan(segy_path)

with pd.option_context("display.max_rows", 100, "display.max_columns", 10):
    # drop byte locations where the mean is zero, these are likely empty.
    display(scan)

scan[scan["mean"] > 0]

scrape = segy_header_scrape(segy_path, partial_scan=1000)
scrape

cube = xr.open_dataset(
    segy_path,
    dim_byte_fields={"iline": 41, "xline": 21},
    extra_byte_fields={"cdp_x": 73, "cdp_y": 77},
)
cube

fig, ax1 = plt.subplots(ncols=1, figsize=(15, 8))
iline_sel = 1400000
cube.data.transpose("samples", "iline", "xline", transpose_coords=True).sel(
    iline=iline_sel
).plot(yincrease=False, cmap="seismic_r")
plt.grid("grey")
plt.ylabel("TWT")
plt.xlabel("XLINE")