import pandas as pd
from bs4 import BeautifulSoup
import json

covid_beds_url = "https://stopcorona.tn.gov.in/beds.php"

import ssl
ssl._create_default_https_context = ssl._create_unverified_context

def process_data():
    import urllib.request
    page = urllib.request.urlopen(covid_beds_url)

    soup = BeautifulSoup(page.read())

    table = soup.find("table", {"id": "dtBasicExample"})
    df = pd.read_html(str(table))[0]

    correct_cols = ["S.NO", "District", "Institution", "Last updated", "Contact Number","Remarks"]

    new_cols = [f"{column[0]}_{column[1]}" if column[0]!=column[1] else column[0] for column in df.columns]
    df.columns = new_cols

    df['Last updated'] = pd.to_datetime(df['Last updated'])
    df['Contact Number'] = df['Contact Number'].astype(str)
    df['Remarks'] = df['Remarks'].astype(str) 

    with open('geo_districts.json',"r") as f:
        data = json.loads(f.read())

    df_geo = pd.DataFrame(data.get('geo_data'))
    print(df_geo.shape)

    df_district = df.groupby('District', as_index=False).sum()
    print(df_district.shape)

    df_district = pd.merge(
        df_district,
        df_geo,
        how="inner",
        left_on="District",
        right_on="district"
    )

    # Save all files
    df.to_csv("tn_covid_beds.csv")
    df_district.to_csv("tn_covid_district_beds.csv")

# Schedule the job
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

from config import DATA_REFRESH_INTERVAL

@sched.scheduled_job('interval', minutes=DATA_REFRESH_INTERVAL)
def timed_job():
    print('The refresh data job is starting now!')
    process_data()
    print(f"Data Refresh was successful!")

if __name__ == '__main__':
    process_data()
    print(f"Data Refresh was successful!")