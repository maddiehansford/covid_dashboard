'''This module handles the collecting and processing of covid data from the
API'''
import json
import logging
from uk_covid19 import Cov19API

FORMAT = '%(levelname)s: %(asctime)s: %(message)s'
logging.basicConfig(filename='log_file.log', format=FORMAT, level=logging.INFO)

with open('config.json') as data_file:
    data = json.load(data_file)
    data = data["misc"]


def parse_csv_data(csv_filename:str) -> list:
    """This function reads from a csv file and returns the content as a list.

    Args:
        csv_filename (str): Name of csv file to be opened

    Returns:
        list: Content of csv file
    """
    parsed_data =[]
    with open(csv_filename) as csv_file:
        for line in csv_file:
            parsed_data.append(line)
    return parsed_data

def process_covid_csv_data(covid_csv_data:list) -> tuple:
    """This function processes the data from static csv file and returns data
    about the last 7 days, current hospital cases and total deaths.

    Args:
        covid_csv_data (list): Content of csv file

    Returns:
        tuple: Integers representing data about last 7 days cases, current
        hospital cases and total deaths
    """
    last7days_cases = 0
    current_hospital_cases = 0
    total_deaths = 0

    #calculates last 7 days cases from file
    for line in range(3, 10):
        data = covid_csv_data[line].split(',')
        last7days_cases += int(data[6])

    #calculates hospital cases from file
    data = covid_csv_data[1].split(',')
    current_hospital_cases = int(data[5])

    #calculates total deaths from file
    data = covid_csv_data[14].split(',')
    total_deaths = int(data[4])

    return last7days_cases, current_hospital_cases, total_deaths

def covid_API_request(location:str = data['location'],
    location_type:str = data['location_type']) -> dict:
    """This function returns live data from the uk-covid19 API.

    Args:
        location (str, optional): Location of data needed from API.
        Defaults to data["location"].
        location_type (str, optional): Type of location need from APi.
        Defaults to data["location_type"].

    Returns:
        dict: Filtered data from covid-19 API
    """
    exeter_only = [
        'areaType='+location_type,
        'areaName='+location
    ]
    cases_and_deaths = {
        "date": "date",
        "areaName": "areaName",
        "newCasesByPublishDate": "newCasesByPublishDate",
        "newCasesBySpecimenDate":"newCasesBySpecimenDate",
        "cumDailyNsoDeathsByDeathDate":"cumDailyNsoDeathsByDeathDate",
        "hospitalCases":"hospitalCases"
    }
    api = Cov19API(filters=exeter_only, structure=cases_and_deaths)
    data = api.get_json(save_as='covid_api_json')
    return data

def local_7_days_extract() -> int:
    """This function extracts and calculates the local cases over the past
    7 days from the covid-api dictionary.

    Returns:
        int: Total local covid cases over past 7 days
    """
    local_7_days = 0
    counter_to_7 = 0
    data_dict = covid_API_request()

    #calculates local data from past 7 days, ignoring any null values
    for day in data_dict['data']:
        if day["newCasesBySpecimenDate"] is not None:
            local_7_days += day["newCasesBySpecimenDate"]
            counter_to_7 +=1
        if counter_to_7 == 7:
            break

    logging.info('LOCAL 7 DAYS REQUEST')
    return local_7_days

def national_7_days_extract() -> int:
    """This function extracts and calculates the national cases over the past
    7 days from the covid-api dictionary.

    Returns:
        int: Total national covid cases over past 7 days
    """
    national_7_days = 0
    counter_to_7 = 0
    data_dict = covid_API_request("England","nation")

    #calculates national data from past 7 days, ignoring any null values
    for day in data_dict['data']:
        if day["newCasesByPublishDate"] is not None:
            national_7_days += day["newCasesByPublishDate"]
            counter_to_7 +=1
        if counter_to_7 == 7:
            break

    logging.info('NATIONAL 7 DAYS REQUEST')
    return national_7_days

def hospital_cases_extract() -> int:
    """This function extracts the total hospital cases from the covid-api
    dictionary.

    Returns:
        int: Covid hospital cases
    """
    hospital_cases = 0
    data_dict = covid_API_request("England","nation")

    #calculates total hospital cases, ignoring any null values
    for day in data_dict['data']:
        if day["hospitalCases"] is not None:
            hospital_cases += day["hospitalCases"]
            break

    logging.info('HOSPITAL CASES REQUEST')
    return hospital_cases

def total_deaths_extract() -> int:
    """This function extracts the total deaths from the covid-api dictionary.

    Returns:
        int: Total covid deaths
    """
    total_deaths = 0
    data_dict = covid_API_request("England","nation")

    #calculates total deaths, ignoring any null values
    for day in data_dict['data']:
        if day["cumDailyNsoDeathsByDeathDate"] is not None:
            total_deaths += day["cumDailyNsoDeathsByDeathDate"]
            break

    logging.info('TOTAL DEATHS REQUEST')
    return total_deaths

def data_gatherer() -> list:
    """This function gathers covid data needed from different functions and
    puts it in a list.

    Returns:
        list: Covid data including local 7 days, national 7 days,
        hospital cases and total deaths
    """
    logging.info('COVID DATA GATHERED')
    return [local_7_days_extract(),national_7_days_extract(),
        hospital_cases_extract(),total_deaths_extract(), data]
