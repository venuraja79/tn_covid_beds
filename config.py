import os

# scheduler job to bed data from tn site
DATA_REFRESH_INTERVAL = os.getenv("DATA_REFRESH_INTERVAL", 180)

COVID_BEDS_URL = os.getenv("COVID_BEDS_URL", "https://stopcorona.tn.gov.in/beds.php")

LOG_LEVEL = os.getenv("LOG_LEVEL","INFO")