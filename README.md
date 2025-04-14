# Downloading LiDAR tiles from the NEON data portal

<p align="center">
    <img src="https://i.imgur.com/waxVImv.png" alt="Oryx EarthDial-ChatGPT">
</p>

This script downloads products from the [NEON (National Ecological Observatory Network)](https://www.neonscience.org/) API for specified sites and years.

## Features

- Downloads `.tif` CHM files from NEON's `DP3.30015.001` product.
- Supports downloading for multiple sites and years.
- Automatically organizes the data by site and date.

## Requirements

Install the required Python packages:

```bash
pip install requests pandas loguru
```

## Usage

```bash
python download_neon_chm.py
```

### Parameters inside the script

- `train_sites` / `test_sites`: List of NEON site codes to download. Can be any four-letter site, amongst which the examples in the script.
- `years`: List of years to download. Use an empty list `[]` to download all available years.
- `save_dir`: Directory path to save the downloaded CHM `.tif` files.

### Example Configuration

```python
train_sites = ['JERC', 'OSBS', 'DELA']
years = []  # Leave empty to get all years
save_dir = '/your/save/path/neon_tiles_train'
```

## Output Structure

The downloaded files will be stored in the following directory structure:

```
save_dir/
├── SITE_CODE/
│   ├── YYYY-MM/
│   │   └── *.tif
```
