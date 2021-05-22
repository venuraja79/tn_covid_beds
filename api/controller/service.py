import logging
from fastapi import APIRouter

from config import (
    LOG_LEVEL,
    COVID_BEDS_URL
)
from bed_data import get_bed_data, get_district_summary

logger = logging.getLogger(__name__)
logger.setLevel(LOG_LEVEL)

router = APIRouter()

@router.post("/api/v1/data")
def get_data():
    '''
    Get the latest covid bed data from covid website
    :return: JSON data
    '''
    try:
        # Scrape and process the data
        df = get_bed_data(COVID_BEDS_URL)
        df_district = get_district_summary(df)
        return {"data": df.to_json(), "summary":df_district.to_json()}
    except Exception as e:
        logger.critical(e, exc_info=True)

