'''Main function that runs the flask app and handles the schedulling of updates'''
import datetime
from datetime import timedelta ,datetime
import sched, time
import logging
from flask import Flask, render_template, request, Markup, redirect
from covid_data_handler import data_gatherer
from covid_news_handling import news_API_request

updates = []
scheduler = sched.scheduler(time.time, time.sleep)
app = Flask('__name__', template_folder = 'template')

FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

@app.route("/")

def home() -> str:
    """This function is the main flask function that renders the index.html
    webpage from ELE.

    Returns:
        str: Front end displaying data from APIs
    """
    scheduler.run(blocking=False)
    return render_template('index.html',
    title = Markup('<b>✻Covid Dashboard✻</b>'),
    location = data_list[4]["location"],
    local_7day_infections = data_list[0],
    nation_location = "England",
    national_7day_infections = data_list[1],
    hospital_cases = "Hospital Cases: " + str(data_list[2]),
    deaths_total = "Total Deaths: " + str(data_list[3]),
    news_articles = news[0:4],
    image = "covidness4.gif",
    updates = updates,
    favicon = "static/images/favicon_tube.png"
    )

@app.route("/index", methods = ['GET'])

def notif_react():
    """This function when directed to /index extention.

    Returns:
        Response: Redirects page to /index when an update is created
        str: Redirects to home function
    """
    scheduler.run(blocking=False)
    update_title = request.args.get('two')
    update_time  = request.args.get('update')

    if 'notif' in request.args:
        #if cancel button clicked in news articles
        logging.info('CANCELLED NEWS')
        title = request.args.get('notif')
        # removes news from list
        for pos, val in enumerate(news):
            if pos < 5 and val['title'] == title:
                news.pop(pos)
            pos += 1

    if 'update_item' in request.args:
        #if cancel button clicked in updates
        logging.info('CANCELLED UPDATE')
        title = request.args.get('update_item')
        # cancels scheduled update & remove update from list
        for pos, val in enumerate(updates):
            if val['title'] == title:
                try:
                    #only if scheduled update hasn't been excecuted
                    scheduler.cancel(val['scheduler'])
                    logging.info('CANCELLED SCHEDULE')
                except:
                    logging.warning('SCHEDULED UPDATE ALREADY EXCECUTED')
                updates.pop(pos)

    if ('covid-data' in request.args) or ('news' in request.args) and ('update' in request.args):
        #when covid-data or news or both are selected to update
        #requests are True if each parameter is selected in update
        covid_data_request = 'covid-data' in request.args
        news_request = 'news' in request.args
        repeat_request = 'repeat' in request.args

        #calculates update interval and creates update
        update_interval = get_update_seconds(update_time)
        new_update = create_update(update_title, update_time,
         repeat_request, covid_data_request,news_request)

        #schedules update
        new_update['scheduler'] = schedule_covid_updates(update_interval,
         new_update['type'],repeat_request)
        updates.append(new_update)

        # redirects page to /index
        return redirect('/index', code=302)

    return home()

def create_update(title:str,time:str,repeat:bool,covid_data:bool,news:bool) -> dict:
    """This method takes elements of an update and formats the update
    description shown to the user, and also assesses the update type.

    Args:
        title (str): Title of update given by user
        time (str): Time of update given by user
        repeat (bool): True if update should be repeated
        covid_data (bool): True if covid data should be updated
        news (bool): True if news should be updated

    Returns:
        dict: The primary element of the update including title,
        formatted content and type
    """
    update_content = Markup('<b>◴   </b>') + time

    #checks whether update is repeated and adds to content accordingly
    if repeat:
        update_content += ' Repeat scheduled update:'
    else:
        update_content += ' Scheduled update:'

    #checks what is being updated and adds to content accordingly
    if covid_data is True and news is True:
        update_content += ' covid data and news.'
        update_type = 'both'
    if covid_data is True and news is False:
        update_content += ' covid data.'
        update_type = 'covid-data'
    if covid_data is False and news is True:
        update_content += ' news.'
        update_type = 'news'

    return {'title':title, 'content':update_content, 'type':update_type}

def schedule_covid_updates(update_interval:int, update_name:str,
    repeat_request:bool=False) -> sched.Event:
    """This function returns a scheduler of a new update.

    Args:
        update_interval (int): Number of seconds until update should be excecuted
        update_name (str): Name of the update, i.e. covid data, news or both
        repeat_request (bool, optional): True if request is repeated. Defaults
        to False.

    Returns:
        sched.Event: Schedulted update event
    """
    return scheduler.enter(update_interval,1,update_excecute,(update_name,repeat_request))

def update_excecute(update_name:str, repeat_request:bool):
    """This function is called by the scheduler when excecuting an update, and
    either updates the news, covid data or both, and repeats if necessary.

    Args:
        update_name (str): Name of update that specifies what should be updates;
        either 'covid-data', 'news' or 'both'
        repeat_request (bool): True if update should be repeated
    """
    if update_name == 'news' or update_name == 'both':
        #changes news seen on home page
        for article in range(0,3):
            news.pop(article)
        logging.info('NEWS')
    if update_name == 'covid-data' or update_name == 'both':
        #updates the data on home page
        data_list = data_gatherer()
        logging.info('COVID DATA')
    if repeat_request:
        #repeats update
        scheduler.enter(86400,1,update_excecute,(update_name,repeat_request))
        logging.info('REPEAT')


def get_update_seconds(str_time: str) -> int:
    """This function calculates the seconds between the current time and the
    scheduled time utelising the datetime module.

    Args:
        str_time (str): Time of scheduled event taken from user input as a
        string

    Returns:
        int: Returns the seconds until the scheduled event should occur
    """
    #creates timedeltas for current time and update time
    interval_bin = datetime(1900,1,1)
    update_time = datetime.strptime(str_time, '%H:%M') - interval_bin
    current_time = datetime.now()
    current_timedelta = timedelta(hours=current_time.hour,
        minutes = current_time.minute, seconds= current_time.second)

    #calculates update interval by comparing the two timedeltas
    if update_time >= current_timedelta:
        update_interval = update_time - current_timedelta
    if update_time < current_timedelta:
        update_time+= timedelta(hours=24)
        update_interval = update_time - current_timedelta
    logging.info('UPDATE INTERVAL: ' + str(update_interval.seconds))

    return update_interval.seconds

if __name__ == "__main__":
    data_list = data_gatherer()
    news = news_API_request()
    app.run(debug=True)
