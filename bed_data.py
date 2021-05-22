import pandas as pd
from bs4 import BeautifulSoup
import json
import logging

import cachetools.func
from retry import retry

import urllib.request

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

from config import COVID_BEDS_URL, DATA_REFRESH_INTERVAL

logger = logging.getLogger(__name__)

def get_bed_data(covid_beds_url):
    page = urllib.request.urlopen(covid_beds_url)

    logger.info(f"Data successfully scraped from {covid_beds_url}")
    soup = BeautifulSoup(page.read())

    table = soup.find("table", {"id": "dtBasicExample"})
    df = pd.read_html(str(table))[0]

    new_cols = [f"{column[0]}_{column[1]}" if column[0]!=column[1] else column[0] for column in df.columns]
    df.columns = new_cols

    df['Last updated'] = pd.to_datetime(df['Last updated'])
    df['Contact Number'] = df['Contact Number'].astype(str)
    df['Remarks'] = df['Remarks'].astype(str)

    return df

def get_district_summary(df):
    with open('./data/geo_districts.json', "r") as f:
        data = json.loads(f.read())

    df_geo = pd.DataFrame(data.get('geo_data'))
    df_district = df.groupby('District', as_index=False).sum()

    df_district = pd.merge(
        df_district,
        df_geo,
        how="inner",
        left_on="District",
        right_on="district"
    )
    logger.info(f"District Summary data size {df_district.shape}")
    return df_district

# TTL in seconds
@cachetools.func.ttl_cache(maxsize=5, ttl=int(DATA_REFRESH_INTERVAL)*60)
@retry(KeyError, tries=3, delay=2)
def refresh_data():
    df = get_bed_data(COVID_BEDS_URL)
    df_dist = get_district_summary(df)

    import datetime
    last_refresh = datetime.datetime.now(datetime.timezone.utc).strftime("%d-%m-%Y %H:%M")
    logger.info(f"Data updated successfully at {last_refresh}")
    return df, df_dist, last_refresh

