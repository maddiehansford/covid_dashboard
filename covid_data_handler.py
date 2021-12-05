from uk_covid19 import Cov19API
import json

with open('config.json') as f:
    data = json.load(f)
    data = data["misc"]

#function 1
def parse_csv_data(csv_filename:str) -> list:
    L =[]
    with open(csv_filename) as f:
        for x in f:
            L.append(x)
    return L

# print(parse_csv_data('nation_2021-10-28.csv'))

#function 2
def process_covid_csv_data(covid_csv_data) -> int:
    last7days_cases = 0
    current_hospital_cases = 0
    total_deaths = 0

    for x in range(3, 10):
        data = covid_csv_data[x].split(',')
        last7days_cases += int(data[6])

    data = covid_csv_data[1].split(',')
    current_hospital_cases = int(data[5])
    
    data = covid_csv_data[14].split(',')
    total_deaths = int(data[4])
   
    return last7days_cases, current_hospital_cases, total_deaths
# process_covid_csv_data(parse_csv_data('nation_2021-10-28.csv'))

#function 3
def covid_API_request(location = data["location"], location_type = data["location_type"]):
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
# print(covid_API_request("England","nation"))

#function 4:
def local_7_days_extract():
    ##extracts local 7 days cases from covid API
    local_7_days = 0
    counter_to_7 = 0
    data_dict = covid_API_request()

    for day in data_dict['data']:
            if day["newCasesBySpecimenDate"] != None:
                local_7_days += day["newCasesBySpecimenDate"]
                counter_to_7 +=1
            if counter_to_7 == 7:
                break
        
    return local_7_days


def national_7_days_extract():
    ##extracts national 7 days cases from covid API
    national_7_days = 0
    counter_to_7 = 0
    data_dict = covid_API_request("England","nation")
    for day in data_dict['data']:
        if day["newCasesByPublishDate"] != None:
            national_7_days += day["newCasesByPublishDate"]
            counter_to_7 +=1
        if counter_to_7 == 7:
            break
        
    return national_7_days

def hospital_cases_extract():
    ##extracts hospital cases from covid API
    hospital_cases = 0
    data_dict = covid_API_request("England","nation")
    for day in data_dict['data']:
            if day["hospitalCases"] != None:
                hospital_cases += day["hospitalCases"]
                break
        
    return hospital_cases

def total_deaths_extract():
    ##extracts total deaths from covid API
    total_deaths = 0
    data_dict = covid_API_request("England","nation")
    for day in data_dict['data']:
            if day["cumDailyNsoDeathsByDeathDate"] != None:
                total_deaths += day["cumDailyNsoDeathsByDeathDate"]
                break
        
    return total_deaths

def data_gatherer():
    ##gathers data and puts it in a list
    return [local_7_days_extract(),national_7_days_extract(),hospital_cases_extract(),total_deaths_extract(), data]


