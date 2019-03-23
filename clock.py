from apscheduler.schedulers.blocking import BlockingScheduler
from mypackage import fgi

sched = BlockingScheduler()

@sched.scheduled_job('interval', seconds=10)
def timed_job():
    print('This job is run every 10 seconds.')
    data = fgi.get_fear_greed_index()[::-1]
    print( data )

@sched.scheduled_job('cron', day_of_week='mon-fri', hour=17)
def scheduled_job():
    print('This job is run every weekday at 5pm.')

sched.start()