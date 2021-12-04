import sched, time
import datetime
from datetime import timedelta, datetime
from covid_data_handler import data_gatherer
from covid_news_handling import news_API_request
scheduler = sched.scheduler(time.time, time.sleep)

def printing():
    print('helo', datetime.time(12,3), str(datetime.datetime.now()), type(datetime.datetime.now()))
    m = 'hi'
    print(datetime.time(int('12:34'[:2]), int('12:34'[3:])))

def poobum():
    scheduler.enter(2, 1, printing, ())
    scheduler.run()

# poobum()

def practice():
    stuff = datetime(1900,1,1)
    update_time = datetime.strptime('12:23', '%H:%M') - stuff 
    print(update_time)


# practice()

def get_update_seconds(str_time):
    

    interval_bin = datetime(1900,1,1)

    update_time = datetime.strptime(str_time, '%H:%M') - interval_bin
    print(update_time)


    current_time = datetime.now()

    current_timedelta = timedelta(hours=current_time.hour, 
    minutes = current_time.minute, seconds= current_time.second)
    print(current_timedelta)

    if (update_time >= current_timedelta):
        update_interval = update_time - current_timedelta
    if (update_time < current_timedelta):
        update_time+= timedelta(hours=24)
        update_interval = update_time - current_timedelta
    
    print(type(update_interval.seconds))


def schedule_covid_updates(update_interval, update_name, repeat = False):
    if (update_name == 'news'):
        scheduler.enter(update_interval,1,update_news,())
    if (update_name == 'covid_data'):
        scheduler.enter(update_interval,1, update_covid_data,())
    if (update_name == 'both'):
        scheduler.enter(update_interval,1, update_both,())
    scheduler.run()

def update_excecute(update_name, repeat):
    if repeat:
        scheduler.enter(86400,1,update_excecute,(update_name,repeat))
    if (update_name == 'news'):
        sdfqsdfasdfasdf



def update_news(repeat):
    print('news')

def update_covid_data(repeat):
    print('covdat')

def update_both(repeat):
    print('both')

def repeating():
    print('repeat')

# schedule_covid_updates(9,'both')
schedule_covid_updates(2,'both')