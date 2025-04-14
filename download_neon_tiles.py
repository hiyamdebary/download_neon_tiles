import requests
import pandas as pd
import os
import re
from loguru import logger

session = requests.Session()

def get_available_data(product_code, site):
    base_url = f"https://data.neonscience.org/api/v0/products/{product_code}"
    try:
        response = session.get(base_url)
        response.raise_for_status() 
        data = response.json()
        return [f for f in data['data']['siteCodes'] if f['siteCode'] == site]
    except requests.RequestException as e:
        logger.info(f"Error fetching data for product {product_code} and site {site}: {e}")
        return []

def download_tif_file(url, save_dir):
    try:
        response = session.get(url)
        response.raise_for_status()
        file_name = os.path.basename(url)
        file_path = os.path.join(save_dir, file_name)
        with open(file_path, 'wb') as file:
            file.write(response.content)
        logger.info(f"File saved to {file_path}")
    except requests.RequestException as e:
        logger.info(f"Failed to download data from {url}: {e}")

def download_chm(product_code, site, year, save_dir):
    available_data = get_available_data(product_code, site)
    if not available_data:
        logger.info(f"No CHM data available for site {site}.")
        return    
    for data in available_data:
        for url_info in data['availableDataUrls']:
            try:
                metadata_response = session.get(url_info)
                metadata_response.raise_for_status()  
                dict_images = metadata_response.json()
                for file_info in dict_images['data']['files']:
                    file_url = file_info['url']
                    if file_url.endswith('.tif'):
                        if year is None:
                            date = dict_images['data']['month']
                        site_dir = os.path.join(save_dir, site, str(date))
                        os.makedirs(site_dir, exist_ok=True)
                        download_tif_file(file_url, site_dir)
            except requests.RequestException as e:
                logger.info(f"Failed to retrieve metadata from {url_info}: {e}")

def download_neon_chm_for_sites_and_years(sites, years, save_dir):
    product_code = "DP3.30015.001"  
    for site in sites:
        if years:
            for year in years:
                logger.info(f"Processing site {site} for year {year}...")
                download_chm(product_code, site, year, save_dir)
        else:
            logger.info(f"Processing site {site} for all available years...")
            download_chm(product_code, site, None, save_dir)

if __name__ == '__main__':
    train_sites = ['JERC', 'OSBS', 'DELA', 'GRSM', 'LENO', 'MLBS', 'BLAN', 'CLBJ', 'KONZ', 'NOGP', 'SCBI', 'TALL', 'UKFS', 'WOOD', 'ABBY', 'BONA', 'DEJU', 'JORN', 'MOAB', 'OAES', 'ONAQ', 'SERC', 'SRER', 'UNDE', 'WREF', 'HEAL', 'LAJA', 'RMNP', 'PUUM']  
    test_sites = ['CUPE', 'REDB', 'WLOU', 'HOPB', 'GUAN']
    years = []  # Keep empty for downloading all available years

    save_dir = 'saving_dir'  
    download_neon_chm_for_sites_and_years(train_sites, years, save_dir)

