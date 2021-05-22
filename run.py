# Scheduler to run in Heroku
# THis is not used any more, instead we will use a cache mechanism

# If you are interested to schedule one in Heroku, please add the below line to Procfile
# clock: python run.py

from bed_data import get_bed_data, get_district_summary
from config import COVID_BEDS_URL

def process_data():
    df = get_bed_data(COVID_BEDS_URL)
    df_district = get_district_summary(df)

    # Save all files
    df.to_csv(path_or_buf="./data/tn_covid_beds.csv", mode='w')
    df_district.to_csv(path_or_buf="./data/tn_covid_district_beds.csv", mode='w')

# Schedule the job
from apscheduler.schedulers.blocking import BlockingScheduler
sched = BlockingScheduler()

from config import DATA_REFRESH_INTERVAL

@sched.scheduled_job('interval', minutes=int(DATA_REFRESH_INTERVAL))
def timed_job():
    print('The refresh data job is starting now!')
    process_data()
    print(f"Data Refresh was successful!")

sched.start()