from os import remove
from flask import Flask, render_template, request, Markup, redirect
from covid_data_handler import data_gatherer
from covid_news_handling import news_API_request
import json, sched, time
import datetime
from datetime import timedelta ,datetime

updates = []
scheduler = sched.scheduler(time.time, time.sleep)
app = Flask('__name__', template_folder = 'template')

@app.route("/")

def home():
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
    updates = updates
    )

@app.route("/index", methods = ['GET'])

def notif_react():
    scheduler.run(blocking=False)
    update_title = request.args.get('two')
    update_time  = request.args.get('update')
    
    ##This code kinda does nothing atm, will be kinda cool when time
    ##till update works tho
    # for update in updates:
    #     new_time = get_update_seconds(update["original_time"])
    #     update["content"] = update["content"].replace(str(time), str(new_time))
    #     update["interval"] = new_time
    
    # while len(updates) > len(scheduler.queue):
    #     removed_updated = updates.pop(0)
    #     if removed_updated["repeat"] == True:
    #         updates.append(removed_updated)
    #         new_time = get_update_seconds(removed_updated["original_time"])
    #         removed_updated["scheduler"] = schedule_covid_updates(new_time, removed_updated["title"])
    
    # print(scheduler.queue)
    
    if 'notif' in request.args:
        ##if cancel button clicked in news articles
        title = request.args.get('notif')
        for pos, val in enumerate(news):
            if pos < 5 and val['title'] == title:
                ## removes news from list
                news.pop(pos)
            pos += 1

    if 'update_item' in request.args:
        ##if cancel button clicked in updates
        title = request.args.get('update_item')
        for pos, val in enumerate(updates):
            if val['title'] == title:
                ## cancels scheduled update & removes update from list
                try:
                    ##only if scheduled update hasn't been excecuted
                    scheduler.cancel(val['scheduler'])
                except:
                    pass
                updates.pop(pos)
                print(scheduler.queue)

    if ('covid-data' in request.args) or ('news' in request.args) and ('update' in request.args):
        covid_data_request = 'covid-data' in request.args
        news_request = 'news' in request.args
        repeat_request = 'repeat' in request.args
        update_interval = get_update_seconds(update_time)


        new_update = create_update(update_title, update_time, repeat_request, covid_data_request,news_request)
        new_update['original_time'] = update_time
        # for update in updates:
        #     if new_update['original_time'] == update['original_time']:
        #         update_interval +=2
        #         print('new update')
        #         print(scheduler.queue)
        
        new_update['scheduler'] = schedule_covid_updates(update_interval,new_update['type'],repeat_request)
        updates.append(new_update) 
        return redirect('/index', code=302)


    return home()
    
def create_update(title,time,repeat,covid_data,news):
    ##formats an update depending on which boxes have been ticked
    update_content = Markup('<b>◴   </b>') + time

    if repeat is True:
        update_content += ' Repeat scheduled update:'
    else:
        update_content += ' Scheduled update:'

    if covid_data is True and news is True:
        update_content += ' covid data and news.'
        update_type = 'both'
    if covid_data is True and news is False:
        update_content += ' covid data.'
        update_type = 'covid-data'
    if covid_data is False and news is True:
        update_content += ' news.'
        update_type = 'news'

    return {'title':title, 'content':update_content, 'repeat_time':time, 'type':update_type}

def schedule_covid_updates(update_interval, update_name, repeat_request=False):
    return scheduler.enter(update_interval,1,update_excecute,(update_name,repeat_request))
    scheduler.run(blocking=False)

def update_excecute(update_name, repeat_request):
    
    if update_name == 'news' or update_name == 'both':
        for article in range(0,3):
            news.pop(article)   
        print('news') 
    if update_name == 'covid-data' or update_name == 'both':
        data_list = data_gatherer()
        print('covid data')
    if repeat_request:
        scheduler.enter(86400,1,update_excecute,(update_name,repeat_request))
        print('repeat')
        print(scheduler.queue)


def get_update_seconds(str_time: str):
    ## takes string of scheduled time from user input on HTML file
    ## calculates seconds until scheduled time from current time

    interval_bin = datetime(1900,1,1)
    update_time = datetime.strptime(str_time, '%H:%M') - interval_bin
    current_time = datetime.now()
    current_timedelta = timedelta(hours=current_time.hour, 
    minutes = current_time.minute, seconds= current_time.second)

    if (update_time >= current_timedelta):
        update_interval = update_time - current_timedelta
    if (update_time < current_timedelta):
        update_time+= timedelta(hours=24)
        update_interval = update_time - current_timedelta
    
    print(update_interval.seconds)
    return update_interval.seconds

def order_updates(update: dict):
    time = update["original_time"].split(':')
    return_time = int(str(time[0] + str(time[1])))
    return return_time

if __name__ == "__main__":
    data_list = data_gatherer()
    news = news_API_request()
    app.run(debug=True)